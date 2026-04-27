# Worker

Scaffold worker Python untuk background loop, heartbeat dasar, dan scheduler tick ringan.

## Isi saat ini

- `app/main.py` untuk loop worker sederhana
- `app/config.py` untuk konfigurasi worker
- `requirements.txt` untuk dependency worker

## Tugas awal worker

- mengecek health backend secara periodik
- menampilkan heartbeat ke log
- memanggil endpoint internal backend untuk scheduler tick berkala
- menjadi titik awal scheduler dan async job berikutnya

## Cara jalan lokal

```bash
pip install -r requirements.txt
python -m app.main
```

## Environment penting

- `BACKEND_URL`
- `WORKER_HEARTBEAT_SECONDS`
- `WORKER_SCHEDULER_INTERVAL_SECONDS`
- `WORKER_API_TOKEN`
