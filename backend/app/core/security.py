import base64
import hashlib
import hmac
import json
from typing import Any

from fastapi import HTTPException, status

from app.core.config import get_settings


def hash_password(password: str) -> str:
    settings = get_settings()
    salted = f"{settings.jwt_secret}:{password}".encode()
    return hashlib.sha256(salted).hexdigest()


def create_access_token(payload: dict[str, Any]) -> str:
    settings = get_settings()
    raw_payload = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    encoded_payload = base64.urlsafe_b64encode(raw_payload).decode().rstrip("=")
    signature = hmac.new(
        settings.jwt_secret.encode(),
        encoded_payload.encode(),
        hashlib.sha256,
    ).hexdigest()
    return f"{encoded_payload}.{signature}"


def decode_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()

    try:
        encoded_payload, signature = token.split(".", maxsplit=1)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token format.",
        ) from exc

    expected_signature = hmac.new(
        settings.jwt_secret.encode(),
        encoded_payload.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token signature.",
        )

    padded_payload = encoded_payload + "=" * (-len(encoded_payload) % 4)
    payload_bytes = base64.urlsafe_b64decode(padded_payload.encode())
    return json.loads(payload_bytes.decode())
