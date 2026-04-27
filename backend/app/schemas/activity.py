from datetime import datetime

from pydantic import BaseModel


class ActivityLogItem(BaseModel):
    id: str
    workspace_id: str
    actor_user_id: str
    category: str
    action: str
    summary: str
    entity_type: str | None = None
    entity_id: str | None = None
    metadata_json: dict[str, object]
    created_at: datetime
    updated_at: datetime
