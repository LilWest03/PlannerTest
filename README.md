# AI Agent Workspace 24/7 untuk Mahasiswa

Scaffold awal untuk proyek workspace berbasis AI agent yang membantu mahasiswa mengelola tugas, dokumen, jadwal, deadline, dan alur kerja belajar secara terstruktur.

## Tujuan Repositori

Repositori ini disiapkan sebagai fondasi implementasi bertahap untuk sistem:

- modular dan mudah dikembangkan
- realistis untuk MVP tugas akhir atau skripsi
- aman untuk operasi penting dengan human-in-the-loop
- mudah diobservasi melalui log, audit trail, dan status task

## Scope Batch 1

Batch pertama berfokus pada bootstrap struktur proyek agar review awal mudah dilakukan:

- penataan folder utama
- dokumentasi dasar proyek
- contoh konfigurasi environment
- docker compose untuk environment lokal
- placeholder per modul agar arah pengembangan jelas

Framework aplikasi inti belum dipasang pada batch ini. Tujuannya agar perubahan awal tetap kecil, jelas, dan mudah direview.

## Struktur Folder

```text
.
├── backend/
├── docs/
├── frontend/
├── infra/
├── scripts/
├── worker/
├── .env.example
└── docker-compose.yml
```

## Gambaran Arsitektur Awal

- `frontend/`: dashboard mahasiswa untuk workspace, task, dokumen, dan status agent
- `backend/`: API utama, auth, workspace orchestration, dan business logic
- `worker/`: background jobs untuk scheduler, indexing dokumen, dan task agent asinkron
- `docs/`: catatan arsitektur, scope MVP, dan dokumentasi teknis
- `infra/`: kebutuhan deployment dan infrastruktur pendukung
- `scripts/`: helper script untuk pengembangan lokal

## Rencana Evolusi Bertahap

### MVP

- autentikasi pengguna
- dashboard workspace dasar
- manajemen task dan deadline
- unggah dan pemrosesan dokumen sederhana
- scheduler task agent dasar

### Versi Menengah

- retrieval context dan memory per workspace
- vector search untuk dokumen kuliah
- notifikasi deadline dan reminder
- observability yang lebih lengkap

### Production-Oriented

- multi-agent orchestration yang lebih matang
- role dan permission yang lebih rinci
- isolasi workload yang lebih baik
- monitoring, retry policy, dan audit trail penuh

## Menjalankan Environment Lokal

1. Salin `.env.example` menjadi `.env`
2. Tinjau nilai environment sesuai kebutuhan lokal
3. Jalankan docker compose:

```bash
docker compose up -d
```

4. Hentikan service:

```bash
docker compose down
```

Catatan: pada batch ini service masih berupa fondasi environment dan placeholder command. Implementasi aplikasi nyata akan ditambahkan pada batch berikutnya.

## Prioritas Batch Berikutnya

- scaffold aplikasi `frontend`
- scaffold API `backend`
- scaffold job runner `worker`
- definisi MVP yang lebih rinci pada `docs/`
- baseline observability dan logging
