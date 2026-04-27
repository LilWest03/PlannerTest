from fastapi import HTTPException, status
from uuid import uuid4

from sqlalchemy.orm import Session

from app.repositories import create_activity_log, get_workspace_by_owner, list_activity_logs_for_workspace
from app.schemas.activity import ActivityLogItem
from app.schemas.auth import AuthUser
from app.services.demo_seed_service import ensure_demo_state


def _to_activity_log_item(activity_log) -> ActivityLogItem:
    return ActivityLogItem(
        id=activity_log.id,
        workspace_id=activity_log.workspace_id,
        actor_user_id=activity_log.actor_user_id,
        category=activity_log.category,
        action=activity_log.action,
        summary=activity_log.summary,
        entity_type=activity_log.entity_type,
        entity_id=activity_log.entity_id,
        metadata_json=activity_log.metadata_json,
        created_at=activity_log.created_at,
        updated_at=activity_log.updated_at,
    )


def record_activity(
    db: Session,
    *,
    workspace_id: str,
    actor_user_id: str,
    category: str,
    action: str,
    summary: str,
    entity_type: str | None = None,
    entity_id: str | None = None,
    metadata_json: dict[str, object] | None = None,
) -> ActivityLogItem:
    activity_log = create_activity_log(
        db,
        activity_log_id=f"alog-{uuid4().hex[:12]}",
        workspace_id=workspace_id,
        actor_user_id=actor_user_id,
        category=category,
        action=action,
        summary=summary,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata_json=metadata_json,
    )
    return _to_activity_log_item(activity_log)


def list_activity_for_workspace(
    db: Session,
    user: AuthUser,
    workspace_id: str,
    *,
    limit: int = 20,
) -> list[ActivityLogItem]:
    ensure_demo_state(db)
    workspace = get_workspace_by_owner(db, user.id)
    if workspace is None or workspace.id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found for this user.",
        )
    logs = list_activity_logs_for_workspace(db, workspace_id, limit=limit)
    return [_to_activity_log_item(log) for log in logs]
