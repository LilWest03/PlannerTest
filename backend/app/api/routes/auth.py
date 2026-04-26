from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user
from app.schemas import AuthResponse, AuthUser, LoginRequest, RegisterRequest
from app.services import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> AuthResponse:
    return register_user(payload)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest) -> AuthResponse:
    return authenticate_user(payload)


@router.get("/me", response_model=AuthUser)
def me(current_user: AuthUser = Depends(get_current_user)) -> AuthUser:
    return current_user
