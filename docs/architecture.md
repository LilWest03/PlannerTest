# Arsitektur Awal

## Prinsip

- modular
- student-centered
- observable
- human-in-the-loop untuk aksi penting
- scalable secara bertahap

## Komponen

### Frontend

Next.js dipakai untuk dashboard mahasiswa, workspace overview, dan titik masuk interaksi dengan agent. Homepage kini login dengan akun demo seeded terlebih dahulu agar alur auth ke workspace bisa didemokan meski database belum aktif.

### Backend API

FastAPI dipakai untuk endpoint utama, orkestrasi request, dan fondasi integrasi antar modul. Baseline saat ini sudah memiliki endpoint health, system summary, auth, dan workspace overview.

### Worker

Worker Python dipakai untuk heartbeat dasar, scheduler, dan proses background yang akan berkembang pada batch berikutnya.

### Database

PostgreSQL tetap menjadi penyimpanan utama untuk data pengguna, workspace, task, dan metadata dokumen. Integrasi database nyata belum diaktifkan; auth dan workspace masih memakai seeded in-memory service layer agar kontrak API bisa direview lebih awal.

### Cache / Queue

Redis dipakai sebagai fondasi queue ringan dan state sementara untuk kebutuhan background process.

## Scope Batch 4

Batch ini mendorong repo dari vertical slice publik ke slice yang sudah punya konteks user:

- backend FastAPI memiliki route `auth`
- utility token bearer ringan berbasis secret aplikasi
- service auth seeded untuk register, login, dan current user
- route `workspaces` sekarang membutuhkan user aktif
- homepage Next.js melakukan demo login sebelum memanggil overview workspace
- compose dan env example mendukung kredensial demo lokal

## Langkah Berikutnya

- persistence auth dan workspace ke PostgreSQL
- migrasi dari token ringan ke JWT yang lebih standar bila diperlukan
- task CRUD dengan relasi ke workspace owner
- integrasi dokumen dan memory
- observability dasar untuk run history
