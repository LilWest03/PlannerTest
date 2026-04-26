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

## Struktur Folder

```text
.
├── backend/
│   ├── app/
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
- `database`: PostgreSQL
- `cache/queue`: Redis

Pilihan ini cukup realistis untuk proyek mahasiswa karena ringan, umum dipakai, dan mudah dikembangkan bertahap.

## Menjalankan Environment Lokal

1. Salin `.env.example` menjadi `.env`
2. Jalankan environment:

```bash
docker compose up --build
```

3. Akses service:

- frontend: `http://localhost:3000`
- backend API: `http://localhost:8000`
- backend docs: `http://localhost:8000/docs`
- workspace overview: `http://localhost:8000/api/v1/workspaces/overview`

4. Hentikan service:

```bash
docker compose down
```

## Gambaran Komponen

- `frontend/`: dashboard awal untuk workspace mahasiswa
- `backend/`: endpoint health, system summary, dan workspace baseline
- `worker/`: background loop awal untuk heartbeat backend
- `docs/`: catatan arsitektur dan scope MVP
- `scripts/`: helper script pengembangan lokal

## Endpoint Awal

- `GET /`
- `GET /api/v1/health`
- `GET /api/v1/system/summary`
- `GET /api/v1/workspaces`
- `GET /api/v1/workspaces/overview`
- `POST /api/v1/workspaces`

## Prioritas Batch Berikutnya

- autentikasi dan ownership workspace
- desain database dan migration awal
- task scheduler yang lebih nyata
- unggah dokumen dan indexing sederhana
- agent run history dan activity log
