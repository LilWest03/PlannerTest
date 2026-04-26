from dataclasses import dataclass
import os


@dataclass
class WorkerSettings:
    backend_url: str = os.getenv("BACKEND_URL", "http://backend:8000")
    heartbeat_seconds: int = int(os.getenv("WORKER_HEARTBEAT_SECONDS", "15"))
    queue_name: str = os.getenv("WORKER_QUEUE_NAME", "agent-jobs")
    app_env: str = os.getenv("APP_ENV", "development")


def get_settings() -> WorkerSettings:
    return WorkerSettings()
