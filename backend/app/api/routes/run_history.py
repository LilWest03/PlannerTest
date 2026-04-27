from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.schemas import AgentRunItem, AuthUser, SchedulerRunItem
from app.services.run_history_service import (
    list_agent_history_for_workspace,
    list_scheduler_history_for_workspace,
)

router = APIRouter(tags=["run-history"])


@router.get("/workspaces/{workspace_id}/scheduler-runs", response_model=list[SchedulerRunItem])
def get_scheduler_runs_for_workspace(
    workspace_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[SchedulerRunItem]:
    return list_scheduler_history_for_workspace(db, current_user, workspace_id, limit=limit)


@router.get("/workspaces/{workspace_id}/agent-runs", response_model=list[AgentRunItem])
def get_agent_runs_for_workspace(
    workspace_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[AgentRunItem]:
    return list_agent_history_for_workspace(db, current_user, workspace_id, limit=limit)
