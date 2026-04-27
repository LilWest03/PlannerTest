from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import SchedulerRun


def list_scheduler_runs_for_workspace(db: Session, workspace_id: str, *, limit: int = 20) -> list[SchedulerRun]:
    statement = (
        select(SchedulerRun)
        .where(SchedulerRun.workspace_id == workspace_id)
        .order_by(SchedulerRun.started_at.desc())
        .limit(limit)
    )
    return list(db.execute(statement).scalars().all())


def create_scheduler_run(
    db: Session,
    *,
    scheduler_run_id: str,
    workspace_id: str,
    owner_id: str,
    job_name: str,
    trigger_type: str,
    status: str,
    summary: str,
    started_at,
    finished_at=None,
) -> SchedulerRun:
    scheduler_run = SchedulerRun(
        id=scheduler_run_id,
        workspace_id=workspace_id,
        owner_id=owner_id,
        job_name=job_name,
        trigger_type=trigger_type,
        status=status,
        summary=summary,
        started_at=started_at,
        finished_at=finished_at,
    )
    db.add(scheduler_run)
    db.commit()
    db.refresh(scheduler_run)
    return scheduler_run
