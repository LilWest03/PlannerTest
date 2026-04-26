from datetime import datetime

from pydantic import BaseModel


class TaskSummary(BaseModel):
    id: str
    title: str
    description: str | None = None
    status: str
    priority: str
    due_at: datetime | None = None
