# Arsitektur Awal

## Prinsip

- modular
- student-centered
- observable
- human-in-the-loop untuk aksi penting
- scalable secara bertahap

## Komponen

### Frontend

Next.js dipakai untuk dashboard mahasiswa, workspace overview, dan titik masuk interaksi dengan agent. Pada baseline ini homepage sudah membaca data overview dari backend untuk menghindari dashboard yang sepenuhnya statis.

### Backend API

FastAPI dipakai untuk endpoint utama, orkestrasi request, dan fondasi integrasi antar modul. Baseline saat ini sudah memiliki endpoint health, system summary, dan workspace overview.

### Worker

Worker Python dipakai untuk heartbeat dasar, scheduler, dan proses background yang akan berkembang pada batch berikutnya.

### Database

PostgreSQL tetap menjadi penyimpanan utama untuk data pengguna, workspace, task, dan metadata dokumen. Integrasi database nyata belum diaktifkan; response workspace masih berupa seeded service layer agar kontrak API bisa ditinjau lebih awal.

### Cache / Queue

Redis dipakai sebagai fondasi queue ringan dan state sementara untuk kebutuhan background process.

## Scope Batch 3

Batch ini mendorong repo dari scaffold generik menuju vertical slice tipis yang sudah bisa ditelusuri dari UI ke API:

- backend FastAPI memiliki route `workspaces`
- service layer dan schema baseline untuk workspace overview
- homepage Next.js membaca data overview dari backend
- docker compose mendukung server-side fetch frontend ke backend
- dokumen scope MVP diperjelas

## Langkah Berikutnya

- auth dan ownership per workspace
- persistence dengan PostgreSQL
- task scheduler yang lebih nyata
- integrasi dokumen dan memory
- observability dasar untuk run history
