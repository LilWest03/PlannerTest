from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.repositories import (
    create_document,
    get_document_for_owner,
    get_workspace_by_owner,
    search_documents_for_workspace,
    list_documents_for_workspace,
)
from app.schemas.auth import AuthUser
from app.schemas.document import (
    DocumentContextMatch,
    DocumentContextResponse,
    DocumentCreateRequest,
    DocumentItem,
    DocumentUploadResponse,
)
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
        retrieval_preview=document.retrieval_preview,
        indexed_at=document.indexed_at,
        retrieval_ready=document.processing_status == "indexed",
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


def _normalize_text(value: str) -> str:
    return " ".join(value.split())


def _build_retrieval_preview(text: str | None, *, limit: int = 220) -> str | None:
    if not text:
        return None

    normalized = _normalize_text(text)
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def _is_text_like(content_type: str, suffix: str) -> bool:
    text_suffixes = {".txt", ".md", ".csv", ".json", ".log", ".py", ".js", ".ts", ".tsx", ".jsx"}
    return content_type.startswith("text/") or suffix.lower() in text_suffixes


def _extract_text_content(safe_original_name: str, content_type: str, content: bytes) -> tuple[str | None, str]:
    suffix = Path(safe_original_name).suffix.lower()
    if not content:
        return None, "needs_review"

    if suffix == ".pdf" or content_type == "application/pdf":
        try:
            from pypdf import PdfReader

            reader = PdfReader(BytesIO(content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            return None, "needs_review"

        normalized = _normalize_text(text)
        if not normalized:
            return None, "needs_review"
        return normalized, "indexed"

    if _is_text_like(content_type, suffix):
        decoded = content.decode("utf-8", errors="ignore")
        normalized = _normalize_text(decoded)
        if not normalized:
            return None, "needs_review"
        return normalized, "indexed"

    return None, "uploaded"


def _build_context_snippet(document, query: str) -> str:
    preview = document.retrieval_preview or ""
    extracted_text = document.extracted_text or preview
    if not extracted_text:
        return "Dokumen belum punya teks yang siap dipakai untuk retrieval."

    lowered_text = extracted_text.lower()
    lowered_query = query.lower()
    index = lowered_text.find(lowered_query)
    if index == -1:
        return preview or extracted_text[:220]

    start = max(0, index - 72)
    end = min(len(extracted_text), index + len(query) + 120)
    snippet = extracted_text[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(extracted_text):
        snippet = snippet + "..."
    return snippet


def _score_context_match(document, query: str) -> int:
    lowered_query = query.lower()
    score = 0
    if lowered_query in document.title.lower():
        score += 3
    if document.extracted_text and lowered_query in document.extracted_text.lower():
        score += 2
    if document.retrieval_preview and lowered_query in document.retrieval_preview.lower():
        score += 1
    if document.indexed_at is not None:
        score += 1
    return score


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


def search_document_context_for_workspace(
    db: Session,
    user: AuthUser,
    workspace_id: str,
    query: str,
    *,
    limit: int = 5,
) -> DocumentContextResponse:
    ensure_demo_state(db)
    _get_owned_workspace(db, user, workspace_id)
    normalized_query = _normalize_text(query)
    if len(normalized_query) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query must contain at least 2 non-space characters.",
        )

    documents = search_documents_for_workspace(db, workspace_id, normalized_query, limit=limit)
    matches = sorted(
        [
            DocumentContextMatch(
                document_id=document.id,
                title=document.title,
                processing_status=document.processing_status,
                retrieval_preview=document.retrieval_preview,
                snippet=_build_context_snippet(document, normalized_query),
                indexed_at=document.indexed_at,
                score=_score_context_match(document, normalized_query),
            )
            for document in documents
        ],
        key=lambda item: (-item.score, item.title.lower()),
    )
    return DocumentContextResponse(
        query=normalized_query,
        total_matches=len(matches),
        matches=matches[:limit],
    )


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
    extracted_text, processing_status = _extract_text_content(safe_original_name, file.content_type or "", content)
    indexed_at = datetime.now(UTC) if processing_status == "indexed" else None
    retrieval_preview = _build_retrieval_preview(extracted_text)
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
        processing_status=processing_status,
        extracted_text=extracted_text,
        retrieval_preview=retrieval_preview,
        indexed_at=indexed_at,
    )
    record_activity(
        db,
        workspace_id=workspace_id,
        actor_user_id=user.id,
        category="document",
        action="document.indexed" if processing_status == "indexed" else "document.uploaded",
        summary=(
            f"Dokumen {document.title} diunggah dan retrieval context siap dipakai."
            if processing_status == "indexed"
            else f"Dokumen {document.title} diunggah ke workspace."
        ),
        entity_type="document",
        entity_id=document.id,
        metadata_json={
            "content_type": document.content_type,
            "size_bytes": document.size_bytes,
            "processing_status": document.processing_status,
            "retrieval_ready": processing_status == "indexed",
        },
    )
    return _to_document_upload_response(document)
