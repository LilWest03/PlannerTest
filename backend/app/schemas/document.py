from datetime import datetime

from pydantic import BaseModel, Field


class DocumentItem(BaseModel):
    id: str
    workspace_id: str
    owner_id: str
    title: str
    original_filename: str
    content_type: str
    size_bytes: int
    processing_status: str
    retrieval_preview: str | None = None
    indexed_at: datetime | None = None
    retrieval_ready: bool
    created_at: datetime
    updated_at: datetime


class DocumentUploadResponse(DocumentItem):
    storage_path: str


class DocumentCreateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=160)


class DocumentContextMatch(BaseModel):
    document_id: str
    title: str
    processing_status: str
    retrieval_preview: str | None = None
    snippet: str
    indexed_at: datetime | None = None
    score: int = Field(..., ge=0)


class DocumentContextResponse(BaseModel):
    query: str
    total_matches: int = Field(..., ge=0)
    matches: list[DocumentContextMatch]
