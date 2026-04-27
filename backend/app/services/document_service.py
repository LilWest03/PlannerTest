from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.repositories import (
    create_document,
    get_document_for_owner,
    get_workspace_by_owner,
    list_documents_for_workspace,
)
from app.schemas.auth import AuthUser
from app.schemas.document import DocumentCreateRequest, DocumentItem, DocumentUploadResponse
from app.services.activity_service import record_activity
from app.services.demo_seed_service import ensure_demo_state


def _to_document_item(document) -> DocumentItem:
    return DocumentItem(
        id=document.id,
        workspace_id=document.workspace_id,
        owner_id=document.owner_id,
        title=document.title,
        original_filename=document.original_filename,
        content_type=document.content_type,
        size_bytes=document.size_bytes,
        processing_status=document.processing_status,
        created_at=document.created_at,
        updated_at=document.updated_at,
    )


def _to_document_upload_response(document) -> DocumentUploadResponse:
    return DocumentUploadResponse(
        **_to_document_item(document).model_dump(),
        storage_path=document.storage_path,
    )


def _get_owned_workspace(db: Session, user: AuthUser, workspace_id: str):
    workspace = get_workspace_by_owner(db, user.id)
    if workspace is None or workspace.id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found for this user.",
        )
    return workspace


def list_documents_for_user_workspace(db: Session, user: AuthUser, workspace_id: str) -> list[DocumentItem]:
    ensure_demo_state(db)
    _get_owned_workspace(db, user, workspace_id)
    documents = list_documents_for_workspace(db, workspace_id)
    return [_to_document_item(document) for document in documents]


def get_document_detail(db: Session, user: AuthUser, document_id: str) -> DocumentItem:
    ensure_demo_state(db)
    document = get_document_for_owner(db, document_id, user.id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
    return _to_document_item(document)


def upload_document_for_workspace(
    db: Session,
    user: AuthUser,
    workspace_id: str,
    payload: DocumentCreateRequest,
    file: UploadFile,
) -> DocumentUploadResponse:
    ensure_demo_state(db)
    _get_owned_workspace(db, user, workspace_id)

    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document filename is required.")

    settings = get_settings()
    document_id = f"doc-{uuid4().hex[:12]}"
    safe_original_name = Path(file.filename).name
    suffix = Path(safe_original_name).suffix
    stored_filename = f"{document_id}{suffix}" if suffix else document_id
    relative_storage_path = Path(settings.storage_path) / user.id / workspace_id
    absolute_storage_dir = Path(__file__).resolve().parents[2] / relative_storage_path
    absolute_storage_dir.mkdir(parents=True, exist_ok=True)
    absolute_storage_path = absolute_storage_dir / stored_filename

    content = file.file.read()
    absolute_storage_path.write_bytes(content)

    document = create_document(
        db,
        document_id=document_id,
        workspace_id=workspace_id,
        owner_id=user.id,
        title=payload.title or Path(safe_original_name).stem,
        original_filename=safe_original_name,
        stored_filename=stored_filename,
        content_type=file.content_type or "application/octet-stream",
        storage_path=str(relative_storage_path / stored_filename),
        size_bytes=len(content),
        processing_status="uploaded",
    )
    record_activity(
        db,
        workspace_id=workspace_id,
        actor_user_id=user.id,
        category="document",
        action="document.uploaded",
        summary=f"Dokumen {document.title} diunggah ke workspace.",
        entity_type="document",
        entity_id=document.id,
        metadata_json={"content_type": document.content_type, "size_bytes": document.size_bytes},
    )
    return _to_document_upload_response(document)
