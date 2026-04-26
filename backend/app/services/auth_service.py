from dataclasses import dataclass
from uuid import uuid4

from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password
from app.schemas.auth import AuthResponse, AuthUser, LoginRequest, RegisterRequest


@dataclass
class StoredUser:
    id: str
    name: str
    email: str
    password_hash: str


_USERS: dict[str, StoredUser] = {
    "demo@mahasiswa.local": StoredUser(
        id="user-demo",
        name="Demo Mahasiswa",
        email="demo@mahasiswa.local",
        password_hash=hash_password("demo12345"),
    )
}


def _to_public_user(user: StoredUser) -> AuthUser:
    return AuthUser(id=user.id, name=user.name, email=user.email)


def register_user(payload: RegisterRequest) -> AuthResponse:
    email = payload.email.lower()

    if email in _USERS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        )

    user = StoredUser(
        id=f"user-{uuid4().hex[:12]}",
        name=payload.name,
        email=email,
        password_hash=hash_password(payload.password),
    )
    _USERS[email] = user
    return issue_auth_response(user)


def authenticate_user(payload: LoginRequest) -> AuthResponse:
    email = payload.email.lower()
    user = _USERS.get(email)

    if user is None or user.password_hash != hash_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return issue_auth_response(user)


def get_user_by_id(user_id: str) -> AuthUser | None:
    for user in _USERS.values():
        if user.id == user_id:
            return _to_public_user(user)
    return None


def issue_auth_response(user: StoredUser) -> AuthResponse:
    public_user = _to_public_user(user)
    token = create_access_token(
        {
            "sub": public_user.id,
            "email": public_user.email,
            "name": public_user.name,
        }
    )
    return AuthResponse(access_token=token, user=public_user)
