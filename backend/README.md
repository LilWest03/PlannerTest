# Backend

Scaffold backend menggunakan FastAPI untuk kebutuhan MVP awal.

## Isi saat ini

- `app/main.py` untuk bootstrap FastAPI
- `app/api/routes/` untuk health, auth, workspace, task CRUD, dan dokumen
- `app/core/config.py` untuk konfigurasi environment
- `app/core/database.py` untuk engine dan session SQLAlchemy
- `app/core/security.py` untuk token bearer ringan scaffold
- `app/models/` untuk model `users`, `workspaces`, `tasks`, `documents`, `activity_logs`, `scheduler_runs`, dan `agent_runs`
- `app/repositories/` untuk akses data user, workspace, task, dokumen, activity log, scheduler run, dan agent run
- `app/services/demo_seed_service.py` untuk seed demo awal ke database dan local storage
- `app/services/task_service.py` untuk task CRUD berbasis owner
- `app/services/document_service.py` untuk upload file dan metadata dokumen
- `app/services/activity_service.py` untuk audit trail activity log workspace
- `app/services/run_history_service.py` untuk histori scheduler run dan agent run
- `app/services/scheduler_service.py` untuk eksekusi scheduler tick dari worker
- `migrations/` + `alembic.ini` untuk migration awal
- `requirements.txt` untuk dependency backend

## Endpoint awal

- `GET /`
- `GET /api/v1/health`
- `GET /api/v1/system/summary`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/workspaces`
- `GET /api/v1/workspaces/overview`
- `POST /api/v1/workspaces`
- `GET /api/v1/workspaces/{workspace_id}/tasks`
- `POST /api/v1/workspaces/{workspace_id}/tasks`
- `GET /api/v1/tasks/{task_id}`
- `PUT /api/v1/tasks/{task_id}`
- `DELETE /api/v1/tasks/{task_id}`
- `GET /api/v1/workspaces/{workspace_id}/documents`
- `POST /api/v1/workspaces/{workspace_id}/documents`
- `GET /api/v1/documents/{document_id}`
- `GET /api/v1/workspaces/{workspace_id}/activity-logs`
- `GET /api/v1/workspaces/{workspace_id}/scheduler-runs`
- `GET /api/v1/workspaces/{workspace_id}/agent-runs`
- `POST /api/v1/workspaces/{workspace_id}/scheduler-runs/trigger`
- `POST /api/v1/internal/scheduler/tick`

## Cara jalan lokal

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Menjalankan migration

Dari folder `backend/` jalankan:

```bash
alembic upgrade head
```

## Catatan

Auth, workspace, task, document metadata, activity log, serta run history sekarang sudah memakai PostgreSQL baseline. File upload disimpan ke local storage awal sesuai `STORAGE_PATH`, demo data observability tetap dibuat saat bootstrap awal, dan worker sudah bisa membuat scheduler run baru lewat route internal bertoken sederhana.
