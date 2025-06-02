"""Database helper functions for **User** objects (async)."""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------


async def get_user(session: AsyncSession, user_id: str) -> User | None:
    """Return user by id or *None*."""

    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """Return user by e-mail or *None*."""

    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def list_users(session: AsyncSession, *, offset: int = 0, limit: int = 100) -> Sequence[User]:
    """Return slice of users ordered by creation date."""

    result = await session.execute(select(User).offset(offset).limit(limit))
    return result.scalars().all()


# ---------------------------------------------------------------------------
# Mutations
# ---------------------------------------------------------------------------


async def create_user(session: AsyncSession, obj_in: UserCreate) -> User:
    """Insert and return a new *User* instance."""

    db_obj = User(
        email=obj_in.email.lower(),
        full_name=obj_in.full_name,
        role=obj_in.role,
        hashed_password=get_password_hash(obj_in.password),
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_user(session: AsyncSession, db_obj: User, obj_in: UserUpdate) -> User:
    """Apply *obj_in* fields onto *db_obj* and persist."""

    if obj_in.full_name is not None:
        db_obj.full_name = obj_in.full_name  # noqa: WPS437
    if obj_in.role is not None:
        db_obj.role = obj_in.role  # noqa: WPS437

    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def delete_user(session: AsyncSession, db_obj: User) -> None:
    """Remove *db_obj* from the database."""

    await session.delete(db_obj)
    await session.commit()
