# Backend

Scaffold backend menggunakan FastAPI untuk kebutuhan MVP awal.

## Isi batch 2

- `app/main.py` untuk bootstrap FastAPI
- `app/api/routes/health.py` untuk endpoint dasar
- `app/core/config.py` untuk konfigurasi environment
- `requirements.txt` untuk dependency backend

## Endpoint awal

- `GET /`
- `GET /api/v1/health`
- `GET /api/v1/system/summary`

## Cara jalan lokal

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
