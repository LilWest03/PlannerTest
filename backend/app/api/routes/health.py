from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "backend",
        "environment": settings.app_env,
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.get("/system/summary")
def system_summary() -> dict[str, object]:
    settings = get_settings()
    return {
        "project": settings.app_name,
        "modules": ["frontend", "backend", "worker", "docs", "workspace-api"],
        "core_features": [
            "task and deadline tracking",
            "workspace overview",
            "agent orchestration baseline",
            "document processing roadmap",
            "workspace summary endpoint",
        ],
        "next_focus": [
            "auth and workspace ownership",
            "database integration",
            "task scheduler",
        ],
    }
