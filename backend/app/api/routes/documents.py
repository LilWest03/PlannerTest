from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.schemas import AuthUser, DocumentCreateRequest, DocumentItem, DocumentUploadResponse
from app.services.document_service import (
    get_document_detail,
    list_documents_for_user_workspace,
    upload_document_for_workspace,
)

router = APIRouter(tags=["documents"])


@router.get("/workspaces/{workspace_id}/documents", response_model=list[DocumentItem])
def get_documents_for_workspace(
    workspace_id: str,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[DocumentItem]:
    return list_documents_for_user_workspace(db, current_user, workspace_id)


@router.post(
    "/workspaces/{workspace_id}/documents",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document_route(
    workspace_id: str,
    title: str | None = Form(default=None),
    file: UploadFile = File(...),
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DocumentUploadResponse:
    payload = DocumentCreateRequest(title=title)
    return upload_document_for_workspace(db, current_user, workspace_id, payload, file)


@router.get("/documents/{document_id}", response_model=DocumentItem)
def get_document_route(
    document_id: str,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DocumentItem:
    return get_document_detail(db, current_user, document_id)
