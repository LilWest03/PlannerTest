# Arsitektur Awal

## Prinsip

- modular
- student-centered
- observable
- human-in-the-loop untuk aksi penting
- scalable secara bertahap

## Komponen

### Frontend

Next.js dipakai untuk dashboard mahasiswa, workspace overview, dan titik masuk interaksi dengan agent. Homepage login dengan akun demo seeded agar alur auth ke workspace bisa didemokan secara konsisten setelah migration database dijalankan.

### Backend API

FastAPI dipakai untuk endpoint utama, orkestrasi request, dan fondasi integrasi antar modul. Baseline saat ini sudah memiliki endpoint health, system summary, auth, workspace overview, task CRUD, dan document upload metadata.

### Worker

Worker Python dipakai untuk heartbeat dasar, scheduler, dan proses background yang akan berkembang pada batch berikutnya.

### Database

PostgreSQL menjadi penyimpanan utama untuk data pengguna, workspace, task, dan metadata dokumen. SQLAlchemy model, repository layer, dan Alembic migration awal sekarang sudah dipakai oleh auth, workspace, task, dan document service dasar.

### Storage

File dokumen disimpan ke local storage baseline melalui `STORAGE_PATH`. Untuk MVP, pendekatan ini cukup sederhana dan realistis sebelum berpindah ke object storage yang lebih kuat.

### Cache / Queue

Redis dipakai sebagai fondasi queue ringan dan state sementara untuk kebutuhan background process.

## Scope Batch 8

Batch ini menambah vertical slice untuk dokumen agar workspace tidak hanya berisi task:

- model dan migration `documents`
- repository untuk metadata dokumen
- endpoint list, upload, dan detail dokumen
- local storage awal untuk file upload
- seeded demo documents agar workspace overview punya angka dokumen nyata
- workspace overview memakai count dokumen aktual dari database

## Langkah Berikutnya

- activity log dasar
- scheduler reminder harian
- document retrieval context dan indexing
- agent run history
- migrasi token ringan ke JWT standar bila dibutuhkan
