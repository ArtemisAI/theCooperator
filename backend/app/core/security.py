"""Password hashing & verification utilities.

Uses **bcrypt** via *passlib* so that we can switch algorithms centrally later.
"""

from passlib.context import CryptContext

import jwt

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud import user as crud_user
from app.db import get_async_session

# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

# The hashing context is instantiated once and reused.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:  # noqa: D401
    """Return *True* if `plain_password` verifies against `hashed_password`."""

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:  # noqa: D401
    """Return *bcrypt* hash for `password`."""

    return pwd_context.hash(password)

# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------

ALGORITHM = "HS256"


def create_access_token(subject: str | dict, expires_delta: timedelta | None = None) -> str:  # noqa: D401
    """Return a signed JWT token."""

    if isinstance(subject, str):
        to_encode: dict = {"sub": subject}
    else:
        to_encode = subject.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    *,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    """Decode JWT and fetch user from DB, raise 401 on failure."""

    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
        subject: str = payload.get("sub")
        if subject is None:
            raise credentials_exc
    except jwt.PyJWTError as exc:  # noqa: WPS433
        raise credentials_exc from exc

    user_obj = await crud_user.get_user(session, subject)
    if user_obj is None:
        raise credentials_exc

    return user_obj

