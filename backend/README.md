# Backend

Scaffold backend menggunakan FastAPI untuk kebutuhan MVP awal.

## Isi saat ini

- `app/main.py` untuk bootstrap FastAPI
- `app/api/routes/` untuk health, auth, dan workspace baseline
- `app/core/config.py` untuk konfigurasi environment
- `app/core/database.py` untuk engine dan session SQLAlchemy
- `app/core/security.py` untuk token bearer ringan scaffold
- `app/models/` untuk model `users`, `workspaces`, dan `tasks`
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

Layer database dan migration sudah siap, tetapi service auth dan workspace saat ini masih memakai seeded in-memory flow. Batch berikutnya perlu menghubungkan service tersebut ke PostgreSQL.
