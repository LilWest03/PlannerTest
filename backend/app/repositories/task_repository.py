from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task


def list_tasks_for_workspace(db: Session, workspace_id: str, *, limit: int = 10) -> list[Task]:
    statement = (
        select(Task)
        .where(Task.workspace_id == workspace_id)
        .order_by(Task.due_at.asc().nullslast(), Task.created_at.asc())
        .limit(limit)
    )
    return list(db.execute(statement).scalars().all())


def create_task(
    db: Session,
    *,
    task_id: str,
    workspace_id: str,
    owner_id: str,
    title: str,
    description: str | None,
    status: str,
    priority: str,
    due_at: datetime | None,
) -> Task:
    task = Task(
        id=task_id,
        workspace_id=workspace_id,
        owner_id=owner_id,
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_at=due_at,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
