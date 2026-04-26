from datetime import UTC, datetime, timedelta

from app.schemas.auth import AuthUser
from app.schemas.workspace import (
    WorkspaceCreateRequest,
    WorkspaceHighlight,
    WorkspaceItem,
    WorkspaceOverview,
    WorkspaceStats,
    WorkspaceTask,
)


def _workspace_item(user: AuthUser) -> WorkspaceItem:
    first_name = user.name.split()[0]
    return WorkspaceItem(
        id=f"ws-{user.id}",
        name=f"Workspace {first_name}",
        description="Ruang kerja untuk tugas, ringkasan dokumen, dan ritme pengerjaan akademik.",
        focus_mode="deadline-aware",
        owner_id=user.id,
        updated_at=datetime.now(UTC),
    )


def list_workspaces(user: AuthUser) -> list[WorkspaceItem]:
    return [_workspace_item(user)]


def get_workspace_overview(user: AuthUser) -> WorkspaceOverview:
    now = datetime.now(UTC)
    first_name = user.name.split()[0]
    return WorkspaceOverview(
        workspace=_workspace_item(user),
        stats=WorkspaceStats(
            active_tasks=6,
            due_today=2,
            active_agents=3,
            indexed_documents=18,
        ),
        upcoming_tasks=[
            WorkspaceTask(
                title=f"Finalkan ringkasan Bab 2 untuk {first_name}",
                course="Metodologi Penelitian",
                due_at=now + timedelta(hours=6),
                priority="high",
                agent_name="Document Agent",
                status="in_review",
            ),
            WorkspaceTask(
                title="Susun timeline eksperimen",
                course="Skripsi",
                due_at=now + timedelta(days=1, hours=2),
                priority="medium",
                agent_name="Task Planner Agent",
                status="queued",
            ),
            WorkspaceTask(
                title="Rapikan catatan jurnal utama",
                course="Natural Language Processing",
                due_at=now + timedelta(days=2),
                priority="medium",
                agent_name="Study Agent",
                status="ready",
            ),
        ],
        highlights=[
            WorkspaceHighlight(
                title="Morning sync selesai",
                detail=f"Deadline {first_name.lower()} hari ini sudah diprioritaskan ulang berdasarkan urgensi tugas.",
                category="scheduler",
            ),
            WorkspaceHighlight(
                title="Dokumen terbaru terindeks",
                detail="Tiga referensi skripsi baru siap dipakai untuk tanya jawab berbasis dokumen.",
                category="documents",
            ),
            WorkspaceHighlight(
                title="Review malam dijadwalkan",
                detail="Agent akan menyiapkan ringkasan progres dan risiko pada pukul 20:00.",
                category="reporting",
            ),
        ],
    )


def create_workspace(payload: WorkspaceCreateRequest, user: AuthUser) -> WorkspaceItem:
    return WorkspaceItem(
        id=f"ws-{user.id}-draft",
        name=payload.name,
        description=payload.description,
        focus_mode=payload.focus_mode,
        owner_id=user.id,
        updated_at=datetime.now(UTC),
    )
