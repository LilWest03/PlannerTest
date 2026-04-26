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


def run() -> None:
    settings = get_settings()
    print(
        f"[worker] queue={settings.queue_name} env={settings.app_env} "
        f"heartbeat={settings.heartbeat_seconds}s"
    )

    while True:
        status = fetch_health(settings.backend_url)
        timestamp = datetime.now(UTC).isoformat()
        print(f"[worker] {timestamp} backend_status={status}")
        sleep(settings.heartbeat_seconds)


if __name__ == "__main__":
    run()
