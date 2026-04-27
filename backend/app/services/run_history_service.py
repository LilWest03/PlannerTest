from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import (
    get_workspace_by_owner,
    list_agent_runs_for_workspace,
    list_scheduler_runs_for_workspace,
)
from app.schemas.auth import AuthUser
from app.schemas.run_history import AgentRunItem, SchedulerRunItem
from app.services.demo_seed_service import ensure_demo_state


def _to_scheduler_run_item(scheduler_run) -> SchedulerRunItem:
    return SchedulerRunItem(
        id=scheduler_run.id,
        workspace_id=scheduler_run.workspace_id,
        owner_id=scheduler_run.owner_id,
        job_name=scheduler_run.job_name,
        trigger_type=scheduler_run.trigger_type,
        status=scheduler_run.status,
        summary=scheduler_run.summary,
        started_at=scheduler_run.started_at,
        finished_at=scheduler_run.finished_at,
        created_at=scheduler_run.created_at,
        updated_at=scheduler_run.updated_at,
    )


def _to_agent_run_item(agent_run) -> AgentRunItem:
    return AgentRunItem(
        id=agent_run.id,
        scheduler_run_id=agent_run.scheduler_run_id,
        workspace_id=agent_run.workspace_id,
        owner_id=agent_run.owner_id,
        agent_key=agent_run.agent_key,
        agent_name=agent_run.agent_name,
        status=agent_run.status,
        target_type=agent_run.target_type,
        target_id=agent_run.target_id,
        summary=agent_run.summary,
        output_summary=agent_run.output_summary,
        started_at=agent_run.started_at,
        finished_at=agent_run.finished_at,
        created_at=agent_run.created_at,
        updated_at=agent_run.updated_at,
    )


def list_scheduler_history_for_workspace(
    db: Session,
    user: AuthUser,
    workspace_id: str,
    *,
    limit: int = 20,
) -> list[SchedulerRunItem]:
    ensure_demo_state(db)
    workspace = get_workspace_by_owner(db, user.id)
    if workspace is None or workspace.id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found for this user.",
        )
    runs = list_scheduler_runs_for_workspace(db, workspace_id, limit=limit)
    return [_to_scheduler_run_item(run) for run in runs]


def list_agent_history_for_workspace(
    db: Session,
    user: AuthUser,
    workspace_id: str,
    *,
    limit: int = 20,
) -> list[AgentRunItem]:
    ensure_demo_state(db)
    workspace = get_workspace_by_owner(db, user.id)
    if workspace is None or workspace.id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found for this user.",
        )
    runs = list_agent_runs_for_workspace(db, workspace_id, limit=limit)
    return [_to_agent_run_item(run) for run in runs]
