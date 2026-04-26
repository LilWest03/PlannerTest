# Worker

Scaffold worker Python untuk background loop dan heartbeat dasar.

## Isi batch 2

- `app/main.py` untuk loop worker sederhana
- `app/config.py` untuk konfigurasi worker
- `requirements.txt` untuk dependency worker

## Tugas awal worker

- mengecek health backend secara periodik
- menampilkan heartbeat ke log
- menjadi titik awal scheduler dan async job berikutnya

## Cara jalan lokal

```bash
pip install -r requirements.txt
python -m app.main
```
