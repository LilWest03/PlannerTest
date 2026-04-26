# Arsitektur Awal

## Prinsip

- modular
- student-centered
- observable
- human-in-the-loop untuk aksi penting
- scalable secara bertahap

## Komponen

### Frontend

Antarmuka mahasiswa untuk mengelola workspace, task, dokumen, deadline, dan interaksi dengan agent.

### Backend API

Layanan utama untuk autentikasi, manajemen workspace, orkestrasi task, dan integrasi antarmodul.

### Worker

Komponen pemrosesan asinkron untuk scheduler, indexing dokumen, dan task jangka panjang.

### Database

Penyimpanan data operasional seperti pengguna, workspace, task, riwayat eksekusi, dan metadata dokumen.

### Cache / Queue

Lapisan pendukung untuk antrian task ringan, koordinasi background jobs, dan state sementara.

## Catatan Batch 1

Dokumen ini masih bersifat fondasi. Diagram, flow task, desain database, dan kontrak API akan dirinci pada batch berikutnya.
