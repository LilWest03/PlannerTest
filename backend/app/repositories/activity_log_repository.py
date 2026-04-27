from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import ActivityLog


def list_activity_logs_for_workspace(db: Session, workspace_id: str, *, limit: int = 20) -> list[ActivityLog]:
    statement = (
        select(ActivityLog)
        .where(ActivityLog.workspace_id == workspace_id)
        .order_by(ActivityLog.created_at.desc())
        .limit(limit)
    )
    return list(db.execute(statement).scalars().all())


def count_activity_logs_for_workspace(db: Session, workspace_id: str) -> int:
    statement = select(func.count(ActivityLog.id)).where(ActivityLog.workspace_id == workspace_id)
    return int(db.execute(statement).scalar_one() or 0)


def create_activity_log(
    db: Session,
    *,
    activity_log_id: str,
    workspace_id: str,
    actor_user_id: str,
    category: str,
    action: str,
    summary: str,
    entity_type: str | None = None,
    entity_id: str | None = None,
    metadata_json: dict[str, object] | None = None,
) -> ActivityLog:
    activity_log = ActivityLog(
        id=activity_log_id,
        workspace_id=workspace_id,
        actor_user_id=actor_user_id,
        category=category,
        action=action,
        summary=summary,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata_json=metadata_json or {},
    )
    db.add(activity_log)
    db.commit()
    db.refresh(activity_log)
    return activity_log
