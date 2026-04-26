# Backend

Scaffold backend menggunakan FastAPI untuk kebutuhan MVP awal.

## Isi saat ini

- `app/main.py` untuk bootstrap FastAPI
- `app/api/routes/` untuk health, auth, workspace, dan task CRUD
- `app/core/config.py` untuk konfigurasi environment
- `app/core/database.py` untuk engine dan session SQLAlchemy
- `app/core/security.py` untuk token bearer ringan scaffold
- `app/models/` untuk model `users`, `workspaces`, dan `tasks`
- `app/repositories/` untuk akses data user, workspace, dan task
- `app/services/demo_seed_service.py` untuk seed demo awal ke database
- `app/services/task_service.py` untuk task CRUD berbasis owner
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

Auth, workspace, dan task service sekarang sudah memakai PostgreSQL baseline. Demo user, workspace, dan task akan dibuat otomatis saat alur auth dipanggil pertama kali setelah database siap.
