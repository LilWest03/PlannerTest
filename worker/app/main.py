from datetime import UTC, datetime
from time import sleep

import requests

from app.config import get_settings


def fetch_health(base_url: str) -> str:
    try:
        response = requests.get(f"{base_url}/api/v1/health", timeout=5)
        response.raise_for_status()
        return response.json().get("status", "unknown")
    except requests.RequestException:
        return "unreachable"


def run_scheduler_tick(base_url: str, worker_api_token: str) -> dict[str, object]:
    try:
        response = requests.post(
            f"{base_url}/api/v1/internal/scheduler/tick",
            headers={"X-Worker-Token": worker_api_token},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        return {"status": "failed", "detail": str(exc)}


def run() -> None:
    settings = get_settings()
    print(
        f"[worker] queue={settings.queue_name} env={settings.app_env} "
        f"heartbeat={settings.heartbeat_seconds}s scheduler_interval={settings.scheduler_interval_seconds}s"
    )
    last_scheduler_run: datetime | None = None

    while True:
        status = fetch_health(settings.backend_url)
        timestamp = datetime.now(UTC).isoformat()
        print(f"[worker] {timestamp} backend_status={status}")
        now = datetime.now(UTC)
        if (
            status == "ok"
            and (
                last_scheduler_run is None
                or (now - last_scheduler_run).total_seconds() >= settings.scheduler_interval_seconds
            )
        ):
            result = run_scheduler_tick(settings.backend_url, settings.worker_api_token)
            print(f"[worker] {timestamp} scheduler_tick={result}")
            if result.get("status") == "ok":
                last_scheduler_run = now
        sleep(settings.heartbeat_seconds)


if __name__ == "__main__":
    run()
