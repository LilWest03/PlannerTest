from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AgentRun


def list_agent_runs_for_workspace(db: Session, workspace_id: str, *, limit: int = 20) -> list[AgentRun]:
    statement = (
        select(AgentRun)
        .where(AgentRun.workspace_id == workspace_id)
        .order_by(AgentRun.started_at.desc())
        .limit(limit)
    )
    return list(db.execute(statement).scalars().all())


def create_agent_run(
    db: Session,
    *,
    agent_run_id: str,
    scheduler_run_id: str | None,
    workspace_id: str,
    owner_id: str,
    agent_key: str,
    agent_name: str,
    status: str,
    target_type: str | None,
    target_id: str | None,
    summary: str,
    output_summary: str | None,
    started_at,
    finished_at=None,
) -> AgentRun:
    agent_run = AgentRun(
        id=agent_run_id,
        scheduler_run_id=scheduler_run_id,
        workspace_id=workspace_id,
        owner_id=owner_id,
        agent_key=agent_key,
        agent_name=agent_name,
        status=status,
        target_type=target_type,
        target_id=target_id,
        summary=summary,
        output_summary=output_summary,
        started_at=started_at,
        finished_at=finished_at,
    )
    db.add(agent_run)
    db.commit()
    db.refresh(agent_run)
    return agent_run
