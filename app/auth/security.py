import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from flask import Response

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_MINUTES = int(os.getenv("JWT_EXP_MINUTES", "60"))
JWT_COOKIE_NAME = os.getenv("JWT_COOKIE_NAME", "auth_token")
JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", "false").lower() == "true"


def create_token(user_id: int, email: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXP_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.InvalidTokenError:
        return None


def set_auth_cookie(response: Response, token: str) -> Response:
    max_age = JWT_EXP_MINUTES * 60 if JWT_EXP_MINUTES > 0 else None
    response.set_cookie(
        JWT_COOKIE_NAME,
        token,
        httponly=True,
        samesite="Lax",
        secure=JWT_COOKIE_SECURE,
        max_age=max_age,
        path="/",
    )
    return response


def clear_auth_cookie(response: Response) -> Response:
    response.delete_cookie(JWT_COOKIE_NAME, path="/")
    return response
