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

FastAPI dipakai untuk endpoint utama, orkestrasi request, dan fondasi integrasi antar modul. Baseline saat ini sudah memiliki endpoint health, system summary, auth, dan workspace overview yang memakai session database.

### Worker

Worker Python dipakai untuk heartbeat dasar, scheduler, dan proses background yang akan berkembang pada batch berikutnya.

### Database

PostgreSQL menjadi penyimpanan utama untuk data pengguna, workspace, dan task. SQLAlchemy model, repository layer, dan Alembic migration awal sekarang sudah dipakai oleh auth dan workspace service dasar.

### Cache / Queue

Redis dipakai sebagai fondasi queue ringan dan state sementara untuk kebutuhan background process.

## Scope Batch 6

Batch ini memindahkan vertical slice awal dari seeded memory ke persistence PostgreSQL:

- repository layer untuk `users`, `workspaces`, dan `tasks`
- auth service register/login/current user memakai database
- workspace service list/create/overview memakai database
- demo user, workspace, dan task di-seed otomatis saat flow auth pertama berjalan
- route auth dan workspace menerima dependency session database
- dokumentasi local setup ikut diperbarui

## Langkah Berikutnya

- task CRUD penuh dengan repository dan schema sendiri
- persistence untuk dokumen dan metadata upload
- activity log dasar
- migrasi token ringan ke JWT standar bila dibutuhkan
- integrasi agent dan document module ke repository layer
