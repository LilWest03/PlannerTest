# Arsitektur Awal

## Prinsip

- modular
- student-centered
- observable
- human-in-the-loop untuk aksi penting
- scalable secara bertahap

## Komponen

### Frontend

Next.js dipakai untuk dashboard mahasiswa, workspace overview, dan titik masuk interaksi dengan agent.

### Backend API

FastAPI dipakai untuk endpoint utama, orkestrasi request, dan fondasi integrasi antar modul.

### Worker

Worker Python dipakai untuk heartbeat dasar, scheduler, dan proses background yang akan berkembang pada batch berikutnya.

### Database

PostgreSQL tetap menjadi penyimpanan utama untuk data pengguna, workspace, task, dan metadata dokumen.

### Cache / Queue

Redis dipakai sebagai fondasi queue ringan dan state sementara untuk kebutuhan background process.

## Scope Batch 2

Batch ini sudah menambahkan scaffold aplikasi inti agar repo tidak lagi hanya berupa placeholder:

- backend FastAPI minimal
- frontend Next.js minimal
- worker Python minimal
- docker compose yang menyiapkan command pengembangan lokal

## Langkah Berikutnya

- desain model database awal
- kontrak API MVP
- task scheduler yang lebih nyata
- integrasi dokumen dan memory
