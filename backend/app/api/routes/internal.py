from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.services.scheduler_service import execute_scheduler_tick

router = APIRouter(prefix="/internal", tags=["internal"])


def verify_worker_token(x_worker_token: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if x_worker_token != settings.worker_api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Worker token is invalid.",
        )


@router.post("/scheduler/tick")
def run_scheduler_tick(
    _: None = Depends(verify_worker_token),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    return execute_scheduler_tick(db)
