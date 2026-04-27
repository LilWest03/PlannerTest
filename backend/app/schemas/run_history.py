from datetime import datetime

from pydantic import BaseModel


class SchedulerRunItem(BaseModel):
    id: str
    workspace_id: str
    owner_id: str
    job_name: str
    trigger_type: str
    status: str
    summary: str
    started_at: datetime
    finished_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class AgentRunItem(BaseModel):
    id: str
    scheduler_run_id: str | None = None
    workspace_id: str
    owner_id: str
    agent_key: str
    agent_name: str
    status: str
    target_type: str | None = None
    target_id: str | None = None
    summary: str
    output_summary: str | None = None
    started_at: datetime
    finished_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
