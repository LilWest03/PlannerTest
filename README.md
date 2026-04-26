# AI Agent Workspace 24/7 untuk Mahasiswa

Scaffold bertahap untuk proyek workspace berbasis AI agent yang membantu mahasiswa mengelola tugas, dokumen, jadwal, deadline, dan alur kerja belajar secara lebih terstruktur.

## Tujuan Repositori

Repositori ini disiapkan sebagai fondasi implementasi bertahap untuk sistem yang:

- modular dan mudah dikembangkan
- realistis untuk MVP tugas akhir atau skripsi
- aman untuk operasi penting dengan human-in-the-loop
- mudah diobservasi melalui log, audit trail, dan status task

## Progress Saat Ini

### Batch 1

- struktur folder utama
- dokumentasi dasar proyek
- contoh konfigurasi environment
- docker compose awal

### Batch 2

- scaffold `backend` dengan FastAPI
- scaffold `frontend` dengan Next.js App Router
- scaffold `worker` dengan Python heartbeat loop
- penyelarasan dokumentasi dan local development flow

### Batch 3

- baseline endpoint `workspace` di backend
- homepage frontend membaca overview dari backend
- dokumentasi scope MVP yang lebih tajam
- compose frontend dibekali `INTERNAL_API_URL` untuk server-side fetch

### Batch 4

- baseline auth dengan bearer token ringan
- seeded demo account untuk login lokal
- endpoint `auth/register`, `auth/login`, dan `auth/me`
- route `workspace` diproteksi dan diikat ke user aktif
- homepage frontend login demo terlebih dahulu sebelum memanggil workspace overview

### Batch 5

- fondasi SQLAlchemy untuk `users`, `workspaces`, dan `tasks`
- session database dan `DATABASE_URL` config
- scaffold Alembic untuk migration
- migration awal pembuatan tabel inti
- compose backend dibekali environment database

### Batch 6

- auth service dipindahkan ke PostgreSQL baseline
- workspace service dipindahkan ke PostgreSQL baseline
- repository layer untuk `user`, `workspace`, dan `task`
- seeded demo user, workspace, dan task dibuat melalui database
- route auth dan workspace sekarang menggunakan session database

### Batch 7

- task CRUD berbasis database
- endpoint list/create task per workspace
- endpoint detail/update/delete task per owner
- schema task untuk create, update, detail, dan summary
- router backend sudah mengekspose modul `tasks`

## Struktur Folder

```text
.
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── alembic.ini
│   └── requirements.txt
├── docs/
├── frontend/
│   ├── app/
│   └── package.json
├── infra/
├── scripts/
├── worker/
│   ├── app/
│   └── requirements.txt
├── .env.example
├── .gitignore
└── docker-compose.yml
```

## Stack Saat Ini

- `frontend`: Next.js 15
- `backend`: FastAPI
- `worker`: Python + requests
- `database`: PostgreSQL + SQLAlchemy + Alembic
- `cache/queue`: Redis

Pilihan ini cukup realistis untuk proyek mahasiswa karena ringan, umum dipakai, dan mudah dikembangkan bertahap.

## Menjalankan Environment Lokal

1. Salin `.env.example` menjadi `.env`
2. Jalankan environment:

```bash
docker compose up --build
```

3. Dari folder `backend/`, jalankan migration awal:

```bash
alembic upgrade head
```

4. Akses service:

- frontend: `http://localhost:3000`
- backend API: `http://localhost:8000`
- backend docs: `http://localhost:8000/docs`
- auth login: `http://localhost:8000/api/v1/auth/login`
- workspace overview: `http://localhost:8000/api/v1/workspaces/overview`
- task list demo: `http://localhost:8000/api/v1/workspaces/ws-user-demo/tasks`

5. Gunakan akun demo lokal:

- email: `demo@mahasiswa.local`
- password: `demo12345`
- name: `Demo Mahasiswa`

6. Hentikan service:

```bash
docker compose down
```

## Gambaran Komponen

- `frontend/`: dashboard awal untuk workspace mahasiswa
- `backend/`: endpoint health, auth, workspace, task CRUD, repository layer, dan persistence PostgreSQL awal
- `worker/`: background loop awal untuk heartbeat backend
- `docs/`: catatan arsitektur dan scope MVP
- `scripts/`: helper script pengembangan lokal

## Endpoint Awal

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

## Prioritas Batch Berikutnya

- document upload dan metadata persistence
- activity log dasar
- scheduler reminder harian
- agent run history
- migrasi token ringan ke JWT standar bila dibutuhkan
