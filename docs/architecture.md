# Architecture Overview

Dokumen ini merangkum arsitektur awal AI Agent Workspace 24/7 untuk Mahasiswa.

## Konteks produk

Workspace ini dirancang sebagai asisten digital mahasiswa yang dapat membantu mengelola pekerjaan akademik, jadwal, catatan, dan proses belajar secara berkelanjutan.

## Komponen utama

```text
[Frontend]
    |
    v
[Backend API] ---> [PostgreSQL]
    |
    v
[Queue / Redis]
    |
    v
[Worker / Agent Runtime]
```

## Peran komponen

### Frontend

Antarmuka utama untuk mahasiswa. Area ini akan menampung dashboard, chat/command center, kalender, daftar tugas, dan insight produktivitas.

### Backend API

Lapisan layanan utama yang menangani autentikasi, data domain, integrasi eksternal, dan orchestration request dari frontend.

### Worker / Agent Runtime

Lapisan eksekusi asynchronous untuk pekerjaan AI agent, sinkronisasi berkala, reminder, dan job panjang.

### PostgreSQL

Penyimpanan data relasional utama untuk user, workspace, tugas, jadwal, catatan, dan konfigurasi agent.

### Redis

Cache dan queue ringan untuk pengembangan lokal. Dapat diganti atau diperkuat sesuai kebutuhan produksi.

## Prinsip desain awal

- Modular sejak awal agar frontend, backend, dan worker dapat berkembang independen.
- Environment lokal harus mudah dijalankan ulang.
- Secret hanya disimpan di `.env`, bukan di repository.
- Keputusan teknis besar harus dicatat di `docs/`.
