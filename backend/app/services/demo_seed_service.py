from datetime import UTC, datetime, timedelta
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.repositories import (
    create_document,
    create_task,
    create_user,
    create_workspace,
    get_document_by_filename,
    get_user_by_email,
    get_workspace_by_owner,
    list_tasks_for_workspace,
)


def ensure_demo_user(db: Session):
    settings = get_settings()
    user = get_user_by_email(db, settings.demo_user_email.lower())
    if user is not None:
        return user

    return create_user(
        db,
        user_id="user-demo",
        name=settings.demo_user_name,
        email=settings.demo_user_email.lower(),
        password_hash=hash_password(settings.demo_user_password),
    )


def ensure_demo_workspace(db: Session, owner_id: str):
    workspace = get_workspace_by_owner(db, owner_id)
    if workspace is not None:
        return workspace

    return create_workspace(
        db,
        workspace_id=f"ws-{owner_id}",
        owner_id=owner_id,
        name="Workspace Demo",
        description="Ruang kerja untuk tugas, ringkasan dokumen, dan ritme pengerjaan akademik.",
        focus_mode="deadline-aware",
    )


def ensure_demo_tasks(db: Session, *, workspace_id: str, owner_id: str) -> None:
    existing_tasks = list_tasks_for_workspace(db, workspace_id, limit=10)
    if existing_tasks:
        return

    now = datetime.now(UTC)
    demo_tasks = [
        {
            "task_id": "task-demo-1",
            "title": "Finalkan ringkasan Bab 2",
            "description": "Rapikan ringkasan metodologi dan poin sitasi utama.",
            "status": "in_review",
            "priority": "high",
            "due_at": now + timedelta(hours=6),
        },
        {
            "task_id": "task-demo-2",
            "title": "Susun timeline eksperimen",
            "description": "Pecah eksperimen skripsi menjadi milestone mingguan.",
            "status": "queued",
            "priority": "medium",
            "due_at": now + timedelta(days=1, hours=2),
        },
        {
            "task_id": "task-demo-3",
            "title": "Rapikan catatan jurnal utama",
            "description": "Kelompokkan catatan referensi NLP untuk review literatur.",
            "status": "ready",
            "priority": "medium",
            "due_at": now + timedelta(days=2),
        },
    ]

    for item in demo_tasks:
        create_task(
            db,
            task_id=item["task_id"],
            workspace_id=workspace_id,
            owner_id=owner_id,
            title=item["title"],
            description=item["description"],
            status=item["status"],
            priority=item["priority"],
            due_at=item["due_at"],
        )


def ensure_demo_documents(db: Session, *, workspace_id: str, owner_id: str) -> None:
    settings = get_settings()
    samples = [
        {
            "document_id": "doc-demo-1",
            "title": "Ringkasan Metodologi",
            "original_filename": "ringkasan-metodologi.txt",
            "content": "Ringkasan metodologi penelitian untuk workspace demo mahasiswa.",
        },
        {
            "document_id": "doc-demo-2",
            "title": "Catatan Literatur NLP",
            "original_filename": "catatan-literatur-nlp.txt",
            "content": "Catatan literatur NLP dasar untuk review literatur dan indexing awal.",
        },
    ]

    base_relative = Path(settings.storage_path) / owner_id / workspace_id
    base_absolute = Path(__file__).resolve().parents[2] / base_relative
    base_absolute.mkdir(parents=True, exist_ok=True)

    for item in samples:
        existing = get_document_by_filename(db, workspace_id, item["original_filename"])
        if existing is not None:
            continue

        stored_filename = item["document_id"] + ".txt"
        absolute_path = base_absolute / stored_filename
        absolute_path.write_text(item["content"], encoding="utf-8")

        create_document(
            db,
            document_id=item["document_id"],
            workspace_id=workspace_id,
            owner_id=owner_id,
            title=item["title"],
            original_filename=item["original_filename"],
            stored_filename=stored_filename,
            content_type="text/plain",
            storage_path=str(base_relative / stored_filename),
            size_bytes=len(item["content"].encode("utf-8")),
            processing_status="indexed",
        )


def ensure_demo_state(db: Session):
    user = ensure_demo_user(db)
    workspace = ensure_demo_workspace(db, user.id)
    ensure_demo_tasks(db, workspace_id=workspace.id, owner_id=user.id)
    ensure_demo_documents(db, workspace_id=workspace.id, owner_id=user.id)
    return user, workspace
