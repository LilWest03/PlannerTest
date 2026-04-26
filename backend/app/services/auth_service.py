from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password
from app.repositories import get_user_by_email, get_user_by_id
from app.schemas.auth import AuthResponse, AuthUser, LoginRequest, RegisterRequest
from app.services.demo_seed_service import ensure_demo_state


def _to_public_user(user) -> AuthUser:
    return AuthUser(id=user.id, name=user.name, email=user.email)


def register_user(db: Session, payload: RegisterRequest) -> AuthResponse:
    ensure_demo_state(db)
    email = payload.email.lower()

    existing_user = get_user_by_email(db, email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        )

    from app.repositories import create_user

    user = create_user(
        db,
        user_id=f"user-{uuid4().hex[:12]}",
        name=payload.name,
        email=email,
        password_hash=hash_password(payload.password),
    )
    return issue_auth_response(user)


def authenticate_user(db: Session, payload: LoginRequest) -> AuthResponse:
    ensure_demo_state(db)
    email = payload.email.lower()
    user = get_user_by_email(db, email)

    if user is None or user.password_hash != hash_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return issue_auth_response(user)


def get_user_by_id_for_auth(db: Session, user_id: str) -> AuthUser | None:
    ensure_demo_state(db)
    user = get_user_by_id(db, user_id)
    if user is None:
        return None
    return _to_public_user(user)


def issue_auth_response(user) -> AuthResponse:
    public_user = _to_public_user(user)
    token = create_access_token(
        {
            "sub": public_user.id,
            "email": public_user.email,
            "name": public_user.name,
        }
    )
    return AuthResponse(access_token=token, user=public_user)
