# AI Agent Workspace 24/7 untuk Mahasiswa

Scaffold awal untuk proyek workspace berbasis AI agent yang membantu mahasiswa mengelola tugas, dokumen, jadwal, deadline, dan alur kerja belajar secara terstruktur.

## Tujuan Repositori

Repositori ini disiapkan sebagai fondasi implementasi bertahap untuk sistem:

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

## Stack Batch 2

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

4. Hentikan service:

```bash
docker compose down
```

## Gambaran Komponen

- `frontend/`: dashboard awal untuk workspace mahasiswa
- `backend/`: endpoint kesehatan sistem dan ringkasan service
- `worker/`: background loop awal untuk heartbeat backend
- `docs/`: catatan arsitektur awal
- `scripts/`: helper script pengembangan lokal

## Endpoint Awal

- `GET /`
- `GET /api/v1/health`
- `GET /api/v1/system/summary`

## Prioritas Batch Berikutnya

- desain database dan migration awal
- kontrak API MVP
- task scheduler yang lebih nyata
- unggah dokumen dan indexing sederhana
- autentikasi dan workspace management
