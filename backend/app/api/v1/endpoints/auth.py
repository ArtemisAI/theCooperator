"""JWT login endpoint."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.crud import user as crud_user
from app.db import get_async_session
from app.schemas.auth import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token, summary="User login")
async def login(
    credentials: LoginRequest, # Moved before session
    *,
    session: AsyncSession = Depends(get_async_session),
) -> Token:
    user = await crud_user.get_user_by_email(session, credentials.email.lower())
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        subject=user.id,
        expires_delta=timedelta(minutes=30),
    )
    return Token(access_token=access_token)
