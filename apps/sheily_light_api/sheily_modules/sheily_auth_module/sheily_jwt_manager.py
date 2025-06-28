from datetime import datetime, timedelta
from jose import jwt
from typing import Any, Dict
from ...core.config import settings

ALGORITHM = "HS256"


def create_access_token(subject: str, expires_delta: int | None = None) -> str:
    """Generate a JWT for a given subject (username)."""
    if expires_delta is None:
        expires_delta = settings.access_token_expire_minutes
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode: Dict[str, Any] = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> str | None:
    """Return subject if token valid, else None."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return str(payload.get("sub"))
    except Exception:
        return None
