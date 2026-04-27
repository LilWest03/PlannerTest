from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.activity import router as activity_router
from app.api.routes.auth import router as auth_router
from app.api.routes.documents import router as document_router
from app.api.routes.health import router as health_router
from app.api.routes.run_history import router as run_history_router
from app.api.routes.tasks import router as task_router
from app.api.routes.workspaces import router as workspace_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.6.0",
    description="Backend API scaffold for AI Agent Workspace 24/7 untuk Mahasiswa.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(workspace_router, prefix=settings.api_prefix)
app.include_router(task_router, prefix=settings.api_prefix)
app.include_router(document_router, prefix=settings.api_prefix)
app.include_router(activity_router, prefix=settings.api_prefix)
app.include_router(run_history_router, prefix=settings.api_prefix)


@app.get("/")
def root() -> dict[str, object]:
    return {
        "message": "AI Agent Workspace backend is running.",
        "docs": "/docs",
        "modules": ["health", "auth", "workspaces", "tasks", "documents", "activity", "run-history"],
    }
