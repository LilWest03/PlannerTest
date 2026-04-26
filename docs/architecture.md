# Arsitektur Awal

## Prinsip

- modular
- student-centered
- observable
- human-in-the-loop untuk aksi penting
- scalable secara bertahap

## Komponen

### Frontend

Next.js dipakai untuk dashboard mahasiswa, workspace overview, dan titik masuk interaksi dengan agent. Homepage kini login dengan akun demo seeded terlebih dahulu agar alur auth ke workspace bisa didemokan meski persistence penuh belum aktif.

### Backend API

FastAPI dipakai untuk endpoint utama, orkestrasi request, dan fondasi integrasi antar modul. Baseline saat ini sudah memiliki endpoint health, system summary, auth, dan workspace overview.

### Worker

Worker Python dipakai untuk heartbeat dasar, scheduler, dan proses background yang akan berkembang pada batch berikutnya.

### Database

PostgreSQL menjadi penyimpanan utama untuk data pengguna, workspace, dan task. Fondasi SQLAlchemy model serta Alembic migration awal sudah ditambahkan agar batch berikutnya bisa langsung menghubungkan service ke persistence nyata.

### Cache / Queue

Redis dipakai sebagai fondasi queue ringan dan state sementara untuk kebutuhan background process.

## Scope Batch 5

Batch ini menyiapkan persistence foundation tanpa memaksa refactor besar di service yang sudah ada:

- config database dan session SQLAlchemy
- model `users`, `workspaces`, dan `tasks`
- scaffold Alembic di folder backend
- migration awal untuk schema inti
- compose backend menerima environment database
- dokumentasi setup migration ikut diperbarui

## Langkah Berikutnya

- ubah auth service dari seeded memory ke repository PostgreSQL
- ubah workspace service agar membaca dan menulis ke database
- tambah task CRUD yang memanfaatkan relasi owner dan workspace
- integrasi dokumen dan memory
- observability dasar untuk run history
