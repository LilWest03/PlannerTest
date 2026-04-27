from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.schemas import AuthUser, TaskCreateRequest, TaskItem, TaskUpdateRequest
from app.services.task_service import (
    create_task_for_workspace,
    delete_task_for_user,
    get_task_detail,
    list_tasks_for_user_workspace,
    update_task_for_user,
)

router = APIRouter(tags=["tasks"])


@router.get("/workspaces/{workspace_id}/tasks", response_model=list[TaskItem])
def get_tasks_for_workspace(
    workspace_id: str,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[TaskItem]:
    return list_tasks_for_user_workspace(db, current_user, workspace_id)


@router.post("/workspaces/{workspace_id}/tasks", response_model=TaskItem, status_code=status.HTTP_201_CREATED)
def create_task_route(
    workspace_id: str,
    payload: TaskCreateRequest,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskItem:
    return create_task_for_workspace(db, current_user, workspace_id, payload)


@router.get("/tasks/{task_id}", response_model=TaskItem)
def get_task_route(
    task_id: str,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskItem:
    return get_task_detail(db, current_user, task_id)


@router.put("/tasks/{task_id}", response_model=TaskItem)
def update_task_route(
    task_id: str,
    payload: TaskUpdateRequest,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskItem:
    return update_task_for_user(db, current_user, task_id, payload)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_route(
    task_id: str,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    delete_task_for_user(db, current_user, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
