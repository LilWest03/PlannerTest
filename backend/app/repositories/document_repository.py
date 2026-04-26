from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Document


def list_documents_for_workspace(db: Session, workspace_id: str, *, limit: int = 50) -> list[Document]:
    statement = (
        select(Document)
        .where(Document.workspace_id == workspace_id)
        .order_by(Document.created_at.desc())
        .limit(limit)
    )
    return list(db.execute(statement).scalars().all())


def get_document_for_owner(db: Session, document_id: str, owner_id: str) -> Document | None:
    statement = select(Document).where(Document.id == document_id, Document.owner_id == owner_id)
    return db.execute(statement).scalar_one_or_none()


def count_documents_for_workspace(db: Session, workspace_id: str) -> int:
    statement = select(func.count(Document.id)).where(Document.workspace_id == workspace_id)
    return int(db.execute(statement).scalar_one() or 0)


def create_document(
    db: Session,
    *,
    document_id: str,
    workspace_id: str,
    owner_id: str,
    title: str,
    original_filename: str,
    stored_filename: str,
    content_type: str,
    storage_path: str,
    size_bytes: int,
    processing_status: str,
) -> Document:
    document = Document(
        id=document_id,
        workspace_id=workspace_id,
        owner_id=owner_id,
        title=title,
        original_filename=original_filename,
        stored_filename=stored_filename,
        content_type=content_type,
        storage_path=storage_path,
        size_bytes=size_bytes,
        processing_status=processing_status,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document
