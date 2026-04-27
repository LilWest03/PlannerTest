from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.schemas import (
    AuthUser,
    WorkspaceCreateRequest,
    WorkspaceItem,
    WorkspaceOverview,
    WorkspaceSchedulerSettings,
    WorkspaceSchedulerSettingsUpdateRequest,
)
from app.services import (
    create_workspace,
    get_workspace_overview,
    get_workspace_scheduler_settings,
    list_workspaces,
    update_workspace_scheduler_settings,
)

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("", response_model=list[WorkspaceItem])
def get_workspaces(
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[WorkspaceItem]:
    return list_workspaces(db, current_user)


@router.get("/overview", response_model=WorkspaceOverview)
def get_overview(
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> WorkspaceOverview:
    return get_workspace_overview(db, current_user)


@router.post("", response_model=WorkspaceItem, status_code=status.HTTP_201_CREATED)
def create_workspace_route(
    payload: WorkspaceCreateRequest,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> WorkspaceItem:
    return create_workspace(db, payload, current_user)


@router.get("/{workspace_id}/scheduler-settings", response_model=WorkspaceSchedulerSettings)
def get_workspace_scheduler_settings_route(
    workspace_id: str,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> WorkspaceSchedulerSettings:
    try:
        return get_workspace_scheduler_settings(db, current_user, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{workspace_id}/scheduler-settings", response_model=WorkspaceSchedulerSettings)
def update_workspace_scheduler_settings_route(
    workspace_id: str,
    payload: WorkspaceSchedulerSettingsUpdateRequest,
    current_user: AuthUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> WorkspaceSchedulerSettings:
    try:
        return update_workspace_scheduler_settings(db, current_user, workspace_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
