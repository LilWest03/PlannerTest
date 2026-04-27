from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.schemas import ActivityLogItem, AuthUser
from app.services.activity_service import list_activity_for_workspace

router = APIRouter(tags=["activity"])


@router.get("/workspaces/{workspace_id}/activity-logs", response_model=list[ActivityLogItem])
def get_activity_logs_for_workspace(
    workspace_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ActivityLogItem]:
    return list_activity_for_workspace(db, current_user, workspace_id, limit=limit)
