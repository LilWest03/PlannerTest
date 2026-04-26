from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Workspace


def list_workspaces_by_owner(db: Session, owner_id: str) -> list[Workspace]:
    statement = select(Workspace).where(Workspace.owner_id == owner_id).order_by(Workspace.created_at.asc())
    return list(db.execute(statement).scalars().all())


def get_workspace_by_owner(db: Session, owner_id: str) -> Workspace | None:
    statement = select(Workspace).where(Workspace.owner_id == owner_id).order_by(Workspace.created_at.asc())
    return db.execute(statement).scalars().first()


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
