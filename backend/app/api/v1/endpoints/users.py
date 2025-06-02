"""REST endpoints for managing **User** entities (Phase 1 backbone).

Routes are mounted under `/api/v1/users`. JWT authentication & RBAC are *not*
implemented at this early stage – they will be added once the basic CRUD
functionality is in place.
"""

from __future__ import annotations

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user as crud_user
from app.db import get_async_session
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


# ---------------------------------------------------------------------------
# Collection routes
# ---------------------------------------------------------------------------


@router.get("/", response_model=list[UserRead], summary="List users")
async def list_users(
    *,
    session: AsyncSession = Depends(get_async_session),
    limit: int = 100,
    offset: int = 0,
) -> Sequence[UserRead]:
    """Return all users.

    Pagination is done via *limit/offset* query-parameters for simplicity.
    """

    return await crud_user.list_users(session, offset=offset, limit=limit)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
    summary="Create user",
)
async def create_user(
    *,
    session: AsyncSession = Depends(get_async_session),
    user_in: UserCreate,
) -> UserRead:
    """Create new user and return it."""

    existing = await crud_user.get_user_by_email(session, user_in.email)
    if existing:
        raise HTTPException(status_code=409, detail="E-mail already registered")

    return await crud_user.create_user(session, user_in)


# ---------------------------------------------------------------------------
# Item routes (by id)
# ---------------------------------------------------------------------------


@router.get("/{user_id}", response_model=UserRead, summary="Get user by id")
async def read_user(
    *,
    session: AsyncSession = Depends(get_async_session),
    user_id: str,
) -> UserRead:
    user = await crud_user.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead, summary="Update user")
async def update_user(
    *,
    session: AsyncSession = Depends(get_async_session),
    user_id: str,
    user_in: UserUpdate,
) -> UserRead:
    db_user = await crud_user.get_user(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return await crud_user.update_user(session, db_user, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user")
async def delete_user(
    *,
    session: AsyncSession = Depends(get_async_session),
    user_id: str,
) -> None:
    db_user = await crud_user.get_user(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    await crud_user.delete_user(session, db_user)
