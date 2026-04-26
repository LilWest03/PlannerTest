from datetime import datetime

from pydantic import BaseModel, Field


class TaskSummary(BaseModel):
    id: str
    title: str
    description: str | None = None
    status: str
    priority: str
    due_at: datetime | None = None


class TaskItem(BaseModel):
    id: str
    workspace_id: str
    owner_id: str
    title: str
    description: str | None = None
    status: str
    priority: str
    due_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=140)
    description: str | None = Field(default=None, max_length=500)
    status: str = Field(default="pending", min_length=3, max_length=32)
    priority: str = Field(default="medium", min_length=3, max_length=32)
    due_at: datetime | None = None


class TaskUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=140)
    description: str | None = Field(default=None, max_length=500)
    status: str | None = Field(default=None, min_length=3, max_length=32)
    priority: str | None = Field(default=None, min_length=3, max_length=32)
    due_at: datetime | None = None
