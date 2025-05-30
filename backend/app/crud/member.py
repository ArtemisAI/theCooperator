"""Database helper functions for **Member** objects (async)."""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Removed: from app.core.security import get_password_hash
from app.models.member import Member # Updated import
from app.schemas.member import MemberCreate, MemberUpdate # Updated import

# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------


async def get_member(session: AsyncSession, member_id: str) -> Member | None:
    """Return member by id or *None*."""

    result = await session.execute(select(Member).where(Member.id == member_id))
    return result.scalar_one_or_none()


async def get_member_by_email(session: AsyncSession, email: str) -> Member | None:
    """Return member by e-mail or *None*."""

    result = await session.execute(select(Member).where(Member.email == email))
    return result.scalar_one_or_none()


async def list_members(session: AsyncSession, *, offset: int = 0, limit: int = 100) -> Sequence[Member]:
    """Return slice of members ordered by creation date."""

    result = await session.execute(select(Member).offset(offset).limit(limit))
    return result.scalars().all()


# ---------------------------------------------------------------------------
# Mutations
# ---------------------------------------------------------------------------


async def create_member(session: AsyncSession, obj_in: MemberCreate) -> Member:
    """Insert and return a new *Member* instance."""
    # Create a dictionary of attributes from obj_in, excluding those not in Member model
    # or handled separately (like password was).
    # MemberCreate inherits from MemberBase.
    member_data = obj_in.dict() # Get all fields from schema
    member_data['email'] = member_data['email'].lower() # Normalize email

    # Ensure all fields in member_data are actual attributes of the Member model
    # This is a simplified approach; a more robust way might involve checking model.__table__.columns
    db_obj = Member(**member_data)

    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_member(session: AsyncSession, db_obj: Member, obj_in: MemberUpdate) -> Member:
    """Apply *obj_in* fields onto *db_obj* and persist."""
    update_data = obj_in.dict(exclude_unset=True)

    if 'email' in update_data:
        update_data['email'] = update_data['email'].lower() # Normalize email if updated

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def delete_member(session: AsyncSession, db_obj: Member) -> None:
    """Remove *db_obj* from the database."""

    await session.delete(db_obj)
    await session.commit()
