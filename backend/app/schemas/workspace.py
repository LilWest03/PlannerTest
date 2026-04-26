from datetime import datetime

from pydantic import BaseModel, Field


class WorkspaceStats(BaseModel):
    active_tasks: int = Field(..., ge=0)
    due_today: int = Field(..., ge=0)
    active_agents: int = Field(..., ge=0)
    indexed_documents: int = Field(..., ge=0)


class WorkspaceTask(BaseModel):
    title: str
    course: str
    due_at: datetime
    priority: str
    agent_name: str
    status: str


class WorkspaceHighlight(BaseModel):
    title: str
    detail: str
    category: str


class WorkspaceItem(BaseModel):
    id: str
    name: str
    description: str
    focus_mode: str
    updated_at: datetime


class WorkspaceOverview(BaseModel):
    workspace: WorkspaceItem
    stats: WorkspaceStats
    upcoming_tasks: list[WorkspaceTask]
    highlights: list[WorkspaceHighlight]


class WorkspaceCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=280)
    focus_mode: str = Field(default="balanced", min_length=3, max_length=40)
