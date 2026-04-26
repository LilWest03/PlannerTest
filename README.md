# AI Agent Workspace 24/7 untuk Mahasiswa

PlannerTest adalah scaffold awal untuk membangun workspace AI agent yang membantu mahasiswa mengelola tugas, jadwal, riset, catatan, dan automasi produktivitas secara 24/7.

## Tujuan awal

- Menyediakan struktur monorepo yang rapi untuk frontend, backend, worker, dokumentasi, infrastruktur, dan script operasional.
- Memisahkan layanan interaktif, API, dan background worker sejak awal.
- Menyediakan konfigurasi lokal berbasis Docker Compose agar mudah dikembangkan ulang oleh kontributor.
- Menjaga perubahan awal tetap kecil, reviewable, dan tidak mengunci pilihan framework terlalu dini.

## Struktur folder

```text
.
├── backend/        # API service dan business logic
├── docs/           # Dokumentasi produk, arsitektur, dan keputusan teknis
├── frontend/       # Web/mobile frontend workspace mahasiswa
├── infra/          # Konfigurasi infrastruktur dan deployment
├── scripts/        # Helper script pengembangan lokal
├── worker/         # Background jobs, scheduler, dan agent runtime
├── .env.example    # Contoh konfigurasi environment
└── docker-compose.yml
```

## Komponen awal

- **Frontend**: antarmuka workspace mahasiswa untuk agenda, tugas, catatan, dan interaksi AI agent.
- **Backend**: API utama untuk autentikasi, data mahasiswa, integrasi, dan orkestrasi agent.
- **Worker**: proses background untuk reminder, sinkronisasi, agent task execution, dan job terjadwal.
- **Infra**: tempat konfigurasi deployment, database, queue, observability, dan IaC.
- **Docs**: dokumentasi arsitektur, product notes, dan runbook.

## Menjalankan lokal

1. Salin konfigurasi environment:

   ```bash
   cp .env.example .env
   ```

2. Jalankan service lokal:

   ```bash
   docker compose up --build
   ```

3. Atau gunakan helper script:

   ```bash
   ./scripts/dev-up.sh
   ./scripts/dev-down.sh
   ```

> Catatan: batch scaffold ini belum memasang framework aplikasi penuh. Service Docker masih berupa placeholder agar struktur repo bisa direview lebih dulu.

## Prinsip pengembangan

- Buat perubahan kecil dan mudah direview.
- Jangan commit secret atau credential ke repo.
- Dokumentasikan keputusan teknis penting di `docs/`.
- Pastikan setiap service punya README lokal ketika mulai diimplementasikan.

## Roadmap scaffold berikutnya

- Pilih stack frontend, misalnya Next.js atau Vite.
- Pilih stack backend, misalnya FastAPI, Express, atau NestJS.
- Tambahkan runtime worker dan queue.
- Tambahkan database lokal dan migration strategy.
- Tambahkan linting, formatting, testing, dan CI.
