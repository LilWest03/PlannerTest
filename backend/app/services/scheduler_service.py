from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import (
    create_agent_run,
    create_scheduler_run,
    get_workspace_by_owner,
    list_tasks_for_workspace,
    list_workspaces,
)
from app.schemas.auth import AuthUser
from app.schemas.run_history import SchedulerTriggerResponse
from app.services.activity_service import record_activity
from app.services.demo_seed_service import ensure_demo_state
from app.services.run_history_service import to_scheduler_run_item


def _execute_scheduler_for_workspace(
    db: Session,
    workspace,
    *,
    trigger_type: str,
    job_name: str,
    run_summary: str,
    activity_action: str,
    activity_summary: str,
    now: datetime,
) -> tuple[object, int]:
    tasks = list_tasks_for_workspace(db, workspace.id, limit=10)
    due_soon_tasks = [
        task for task in tasks if task.due_at is not None and task.due_at <= now + timedelta(hours=24)
    ][:2]

    scheduler_run = create_scheduler_run(
        db,
        scheduler_run_id=f"srun-{uuid4().hex[:12]}",
        workspace_id=workspace.id,
        owner_id=workspace.owner_id,
        job_name=job_name,
        trigger_type=trigger_type,
        status="success",
        summary=run_summary,
        started_at=now,
        finished_at=now + timedelta(seconds=2),
    )

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

    agent_runs_created = len(due_soon_tasks) if due_soon_tasks else 1
    record_activity(
        db,
        workspace_id=workspace.id,
        actor_user_id=workspace.owner_id,
        category="scheduler",
        action=activity_action,
        summary=activity_summary,
        entity_type="scheduler_run",
        entity_id=scheduler_run.id,
        metadata_json={
            "job_name": scheduler_run.job_name,
            "trigger_type": trigger_type,
            "agent_runs_created": agent_runs_created,
        },
    )
    return scheduler_run, agent_runs_created


def execute_scheduler_tick(db: Session) -> dict[str, object]:
    ensure_demo_state(db)
    workspaces = list_workspaces(db)
    processed_workspaces = 0
    scheduler_run_count = 0
    agent_run_count = 0
    now = datetime.now(UTC)

    for workspace in workspaces:
        processed_workspaces += 1
        _, workspace_agent_runs = _execute_scheduler_for_workspace(
            db,
            workspace,
            trigger_type="worker",
            job_name="daily-reminder",
            run_summary="Worker menjalankan scheduler reminder harian untuk memeriksa task prioritas workspace.",
            activity_action="scheduler.worker_tick",
            activity_summary="Worker menjalankan scheduler tick dan memperbarui histori run workspace.",
            now=now,
        )
        scheduler_run_count += 1
        agent_run_count += workspace_agent_runs

    return {
        "status": "ok",
        "processed_workspaces": processed_workspaces,
        "scheduler_runs_created": scheduler_run_count,
        "agent_runs_created": agent_run_count,
        "executed_at": now.isoformat(),
    }


def execute_manual_scheduler_run(
    db: Session,
    user: AuthUser,
    workspace_id: str,
) -> SchedulerTriggerResponse:
    ensure_demo_state(db)
    workspace = get_workspace_by_owner(db, user.id)
    if workspace is None or workspace.id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found for this user.",
        )

    now = datetime.now(UTC)
    scheduler_run, agent_runs_created = _execute_scheduler_for_workspace(
        db,
        workspace,
        trigger_type="manual",
        job_name="manual-refresh",
        run_summary="Pengguna memicu scheduler workspace secara manual dari dashboard untuk menyegarkan prioritas akademik.",
        activity_action="scheduler.manual_triggered",
        activity_summary="Pengguna menjalankan scheduler manual dari dashboard workspace.",
        now=now,
    )

    return SchedulerTriggerResponse(
        status="ok",
        workspace_id=workspace.id,
        scheduler_run=to_scheduler_run_item(scheduler_run),
        agent_runs_created=agent_runs_created,
        executed_at=now,
    )
