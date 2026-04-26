from datetime import UTC, datetime, timedelta

from app.schemas.workspace import (
    WorkspaceCreateRequest,
    WorkspaceHighlight,
    WorkspaceItem,
    WorkspaceOverview,
    WorkspaceStats,
    WorkspaceTask,
)


def _workspace_item() -> WorkspaceItem:
    return WorkspaceItem(
        id="ws-skripsi-ai",
        name="Workspace Skripsi AI",
        description="Ruang kerja untuk tugas, ringkasan dokumen, dan ritme pengerjaan skripsi.",
        focus_mode="deadline-aware",
        updated_at=datetime.now(UTC),
    )


def list_workspaces() -> list[WorkspaceItem]:
    return [_workspace_item()]


def get_workspace_overview() -> WorkspaceOverview:
    now = datetime.now(UTC)
    return WorkspaceOverview(
        workspace=_workspace_item(),
        stats=WorkspaceStats(
            active_tasks=6,
            due_today=2,
            active_agents=3,
            indexed_documents=18,
        ),
        upcoming_tasks=[
            WorkspaceTask(
                title="Finalkan ringkasan Bab 2",
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
                detail="Deadline hari ini sudah diprioritaskan ulang berdasarkan urgensi tugas.",
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


def create_workspace(payload: WorkspaceCreateRequest) -> WorkspaceItem:
    return WorkspaceItem(
        id="ws-draft-new",
        name=payload.name,
        description=payload.description,
        focus_mode=payload.focus_mode,
        updated_at=datetime.now(UTC),
    )
