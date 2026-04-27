from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Workspace


def list_workspaces(db: Session) -> list[Workspace]:
    statement = select(Workspace).order_by(Workspace.created_at.asc())
    return list(db.execute(statement).scalars().all())


def list_workspaces_by_owner(db: Session, owner_id: str) -> list[Workspace]:
    statement = select(Workspace).where(Workspace.owner_id == owner_id).order_by(Workspace.created_at.asc())
    return list(db.execute(statement).scalars().all())


def get_workspace_by_owner(db: Session, owner_id: str) -> Workspace | None:
    statement = select(Workspace).where(Workspace.owner_id == owner_id).order_by(Workspace.created_at.asc())
    return db.execute(statement).scalars().first()


def get_workspace_for_owner(db: Session, workspace_id: str, owner_id: str) -> Workspace | None:
    statement = select(Workspace).where(Workspace.id == workspace_id, Workspace.owner_id == owner_id)
    return db.execute(statement).scalar_one_or_none()


def create_workspace(
    db: Session,
    *,
    workspace_id: str,
    owner_id: str,
    name: str,
    description: str,
    focus_mode: str,
) -> Workspace:
    workspace = Workspace(
        id=workspace_id,
        owner_id=owner_id,
        name=name,
        description=description,
        focus_mode=focus_mode,
    )
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace


def update_workspace_scheduler_settings(
    db: Session,
    workspace: Workspace,
    *,
    scheduler_enabled: bool | None,
    reminder_window_hours: int | None,
    max_tasks_per_run: int | None,
) -> Workspace:
    if scheduler_enabled is not None:
        workspace.scheduler_enabled = scheduler_enabled
    if reminder_window_hours is not None:
        workspace.reminder_window_hours = reminder_window_hours
    if max_tasks_per_run is not None:
        workspace.max_tasks_per_run = max_tasks_per_run

    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace
