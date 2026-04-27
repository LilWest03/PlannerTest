from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import (
    create_task,
    delete_task,
    get_task_for_owner,
    get_workspace_by_owner,
    list_tasks_for_workspace,
    update_task,
)
from app.schemas.auth import AuthUser
from app.schemas.task import TaskCreateRequest, TaskItem, TaskUpdateRequest
from app.services.activity_service import record_activity
from app.services.demo_seed_service import ensure_demo_state


def _to_task_item(task) -> TaskItem:
    return TaskItem(
        id=task.id,
        workspace_id=task.workspace_id,
        owner_id=task.owner_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_at=task.due_at,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


def _get_owned_workspace(db: Session, user: AuthUser, workspace_id: str):
    workspace = get_workspace_by_owner(db, user.id)
    if workspace is None or workspace.id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found for this user.",
        )
    return workspace


def list_tasks_for_user_workspace(db: Session, user: AuthUser, workspace_id: str) -> list[TaskItem]:
    ensure_demo_state(db)
    _get_owned_workspace(db, user, workspace_id)
    tasks = list_tasks_for_workspace(db, workspace_id, limit=100)
    return [_to_task_item(task) for task in tasks]


def create_task_for_workspace(
    db: Session,
    user: AuthUser,
    workspace_id: str,
    payload: TaskCreateRequest,
) -> TaskItem:
    ensure_demo_state(db)
    _get_owned_workspace(db, user, workspace_id)
    task = create_task(
        db,
        task_id=f"task-{uuid4().hex[:12]}",
        workspace_id=workspace_id,
        owner_id=user.id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        due_at=payload.due_at,
    )
    record_activity(
        db,
        workspace_id=workspace_id,
        actor_user_id=user.id,
        category="task",
        action="task.created",
        summary=f"Task {task.title} ditambahkan ke workspace.",
        entity_type="task",
        entity_id=task.id,
        metadata_json={"status": task.status, "priority": task.priority},
    )
    return _to_task_item(task)


def get_task_detail(db: Session, user: AuthUser, task_id: str) -> TaskItem:
    ensure_demo_state(db)
    task = get_task_for_owner(db, task_id, user.id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return _to_task_item(task)


def update_task_for_user(
    db: Session,
    user: AuthUser,
    task_id: str,
    payload: TaskUpdateRequest,
) -> TaskItem:
    ensure_demo_state(db)
    task = get_task_for_owner(db, task_id, user.id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    updated_task = update_task(
        db,
        task,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        due_at=payload.due_at,
        due_at_provided="due_at" in payload.model_fields_set,
    )
    record_activity(
        db,
        workspace_id=updated_task.workspace_id,
        actor_user_id=user.id,
        category="task",
        action="task.updated",
        summary=f"Task {updated_task.title} diperbarui di workspace.",
        entity_type="task",
        entity_id=updated_task.id,
        metadata_json={"status": updated_task.status, "priority": updated_task.priority},
    )
    return _to_task_item(updated_task)


def delete_task_for_user(db: Session, user: AuthUser, task_id: str) -> None:
    ensure_demo_state(db)
    task = get_task_for_owner(db, task_id, user.id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    record_activity(
        db,
        workspace_id=task.workspace_id,
        actor_user_id=user.id,
        category="task",
        action="task.deleted",
        summary=f"Task {task.title} dihapus dari workspace.",
        entity_type="task",
        entity_id=task.id,
        metadata_json={"status": task.status},
    )
    delete_task(db, task)
