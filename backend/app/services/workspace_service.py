from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.repositories import (
    count_documents_for_workspace,
    create_workspace as create_workspace_record,
    get_workspace_by_owner,
    list_tasks_for_workspace,
    list_workspaces_by_owner,
)
from app.schemas.auth import AuthUser
from app.schemas.workspace import (
    WorkspaceCreateRequest,
    WorkspaceHighlight,
    WorkspaceItem,
    WorkspaceOverview,
    WorkspaceStats,
    WorkspaceTask,
)
from app.services.activity_service import record_activity
from app.services.demo_seed_service import ensure_demo_state


def _to_workspace_item(workspace) -> WorkspaceItem:
    return WorkspaceItem(
        id=workspace.id,
        name=workspace.name,
        description=workspace.description,
        focus_mode=workspace.focus_mode,
        owner_id=workspace.owner_id,
        updated_at=workspace.updated_at,
    )


def list_workspaces(db: Session, user: AuthUser) -> list[WorkspaceItem]:
    ensure_demo_state(db)
    workspaces = list_workspaces_by_owner(db, user.id)
    return [_to_workspace_item(workspace) for workspace in workspaces]


def get_workspace_overview(db: Session, user: AuthUser) -> WorkspaceOverview:
    ensure_demo_state(db)
    workspace = get_workspace_by_owner(db, user.id)
    if workspace is None:
        workspace = create_workspace_record(
            db,
            workspace_id=f"ws-{uuid4().hex[:12]}",
            owner_id=user.id,
            name=f"Workspace {user.name.split()[0]}",
            description="Ruang kerja untuk tugas, ringkasan dokumen, dan ritme pengerjaan akademik.",
            focus_mode="deadline-aware",
        )

    tasks = list_tasks_for_workspace(db, workspace.id, limit=6)
    document_count = count_documents_for_workspace(db, workspace.id)
    due_today = 0
    now = datetime.now(UTC).date()
    upcoming_tasks: list[WorkspaceTask] = []
    for task in tasks:
        if task.due_at and task.due_at.date() == now:
            due_today += 1
        upcoming_tasks.append(
            WorkspaceTask(
                title=task.title,
                course="Workspace Akademik",
                due_at=task.due_at or workspace.updated_at,
                priority=task.priority,
                agent_name="Task Planner Agent",
                status=task.status,
            )
        )

    first_name = user.name.split()[0]
    return WorkspaceOverview(
        workspace=_to_workspace_item(workspace),
        stats=WorkspaceStats(
            active_tasks=len(tasks),
            due_today=due_today,
            active_agents=3,
            indexed_documents=document_count,
        ),
        upcoming_tasks=upcoming_tasks,
        highlights=[
            WorkspaceHighlight(
                title="Workspace tersinkron",
                detail=f"Data workspace {first_name.lower()} sekarang dibaca dari PostgreSQL baseline.",
                category="database",
            ),
            WorkspaceHighlight(
                title="Task prioritas tersedia",
                detail="Task demo awal tersimpan sebagai data dasar untuk pengembangan CRUD berikutnya.",
                category="tasks",
            ),
            WorkspaceHighlight(
                title="Dokumen siap dipakai",
                detail=f"{document_count} dokumen sudah tercatat dan siap dipakai untuk indexing lanjutan.",
                category="documents",
            ),
            WorkspaceHighlight(
                title="Observability dasar aktif",
                detail="Activity log, scheduler run, dan agent run history siap dipakai untuk audit trail MVP.",
                category="observability",
            ),
        ],
    )


def create_workspace(db: Session, payload: WorkspaceCreateRequest, user: AuthUser) -> WorkspaceItem:
    ensure_demo_state(db)
    workspace = create_workspace_record(
        db,
        workspace_id=f"ws-{uuid4().hex[:12]}",
        owner_id=user.id,
        name=payload.name,
        description=payload.description,
        focus_mode=payload.focus_mode,
    )
    record_activity(
        db,
        workspace_id=workspace.id,
        actor_user_id=user.id,
        category="workspace",
        action="workspace.created",
        summary=f"Workspace {workspace.name} dibuat untuk ritme kerja akademik baru.",
        entity_type="workspace",
        entity_id=workspace.id,
        metadata_json={"focus_mode": workspace.focus_mode},
    )
    return _to_workspace_item(workspace)
