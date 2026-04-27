from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from app.repositories import (
    create_agent_run,
    create_scheduler_run,
    list_tasks_for_workspace,
    list_workspaces,
)
from app.services.activity_service import record_activity
from app.services.demo_seed_service import ensure_demo_state


def execute_scheduler_tick(db: Session) -> dict[str, object]:
    ensure_demo_state(db)
    workspaces = list_workspaces(db)
    processed_workspaces = 0
    scheduler_run_count = 0
    agent_run_count = 0
    now = datetime.now(UTC)

    for workspace in workspaces:
        processed_workspaces += 1
        tasks = list_tasks_for_workspace(db, workspace.id, limit=10)
        due_soon_tasks = [
            task
            for task in tasks
            if task.due_at is not None and task.due_at <= now + timedelta(hours=24)
        ][:2]

        scheduler_run = create_scheduler_run(
            db,
            scheduler_run_id=f"srun-{uuid4().hex[:12]}",
            workspace_id=workspace.id,
            owner_id=workspace.owner_id,
            job_name="daily-reminder",
            trigger_type="worker",
            status="success",
            summary="Worker menjalankan scheduler reminder harian untuk memeriksa task prioritas workspace.",
            started_at=now,
            finished_at=now + timedelta(seconds=2),
        )
        scheduler_run_count += 1

        if due_soon_tasks:
            for task in due_soon_tasks:
                create_agent_run(
                    db,
                    agent_run_id=f"arun-{uuid4().hex[:12]}",
                    scheduler_run_id=scheduler_run.id,
                    workspace_id=workspace.id,
                    owner_id=workspace.owner_id,
                    agent_key="deadline-brief",
                    agent_name="Deadline Brief Agent",
                    status="success",
                    target_type="task",
                    target_id=task.id,
                    summary=f"Agent meninjau task {task.title} yang mendekati deadline.",
                    output_summary=f"Task {task.title} perlu masuk shortlist reminder 24 jam.",
                    started_at=now,
                    finished_at=now + timedelta(seconds=1),
                )
                agent_run_count += 1
        else:
            create_agent_run(
                db,
                agent_run_id=f"arun-{uuid4().hex[:12]}",
                scheduler_run_id=scheduler_run.id,
                workspace_id=workspace.id,
                owner_id=workspace.owner_id,
                agent_key="study-rhythm",
                agent_name="Study Rhythm Agent",
                status="success",
                target_type="workspace",
                target_id=workspace.id,
                summary="Agent membuat rekomendasi ritme belajar saat tidak ada deadline dekat.",
                output_summary="Sesi fokus baru bisa dijadwalkan karena tidak ada task yang jatuh tempo dalam 24 jam.",
                started_at=now,
                finished_at=now + timedelta(seconds=1),
            )
            agent_run_count += 1

        record_activity(
            db,
            workspace_id=workspace.id,
            actor_user_id=workspace.owner_id,
            category="scheduler",
            action="scheduler.worker_tick",
            summary="Worker menjalankan scheduler tick dan memperbarui histori run workspace.",
            entity_type="scheduler_run",
            entity_id=scheduler_run.id,
            metadata_json={
                "job_name": scheduler_run.job_name,
                "agent_runs_created": len(due_soon_tasks) if due_soon_tasks else 1,
            },
        )

    return {
        "status": "ok",
        "processed_workspaces": processed_workspaces,
        "scheduler_runs_created": scheduler_run_count,
        "agent_runs_created": agent_run_count,
        "executed_at": now.isoformat(),
    }
