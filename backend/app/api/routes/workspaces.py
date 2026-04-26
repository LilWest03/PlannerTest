from fastapi import APIRouter, status

from app.schemas import WorkspaceCreateRequest, WorkspaceItem, WorkspaceOverview
from app.services import create_workspace, get_workspace_overview, list_workspaces

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("", response_model=list[WorkspaceItem])
def get_workspaces() -> list[WorkspaceItem]:
    return list_workspaces()


@router.get("/overview", response_model=WorkspaceOverview)
def get_overview() -> WorkspaceOverview:
    return get_workspace_overview()


@router.post("", response_model=WorkspaceItem, status_code=status.HTTP_201_CREATED)
def create_workspace_route(payload: WorkspaceCreateRequest) -> WorkspaceItem:
    return create_workspace(payload)
