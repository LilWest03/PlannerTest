from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.schemas import AuthUser, WorkspaceCreateRequest, WorkspaceItem, WorkspaceOverview
from app.services import create_workspace, get_workspace_overview, list_workspaces

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
