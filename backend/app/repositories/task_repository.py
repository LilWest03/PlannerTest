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


def get_task_by_id(db: Session, task_id: str) -> Task | None:
    statement = select(Task).where(Task.id == task_id)
    return db.execute(statement).scalar_one_or_none()


def get_task_for_owner(db: Session, task_id: str, owner_id: str) -> Task | None:
    statement = select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
    return db.execute(statement).scalar_one_or_none()


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


def update_task(
    db: Session,
    task: Task,
    *,
    title: str | None,
    description: str | None,
    status: str | None,
    priority: str | None,
    due_at: datetime | None,
    due_at_provided: bool,
) -> Task:
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if status is not None:
        task.status = status
    if priority is not None:
        task.priority = priority
    if due_at_provided:
        task.due_at = due_at

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
