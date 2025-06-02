"""Async CRUD helpers for the **Unit** model."""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.unit import Unit
from app.schemas.unit import UnitCreate, UnitUpdate


async def get_unit(session: AsyncSession, unit_id: str) -> Unit | None:
    result = await session.execute(select(Unit).where(Unit.id == unit_id))
    return result.scalar_one_or_none()


async def list_units(session: AsyncSession, *, offset: int = 0, limit: int = 100) -> Sequence[Unit]:
    result = await session.execute(select(Unit).offset(offset).limit(limit))
    return result.scalars().all()


async def create_unit(session: AsyncSession, obj_in: UnitCreate) -> Unit:
    db_obj = Unit(label=obj_in.label)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_unit(session: AsyncSession, db_obj: Unit, obj_in: UnitUpdate) -> Unit:
    if obj_in.label is not None:
        db_obj.label = obj_in.label  # noqa: WPS437

    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def delete_unit(session: AsyncSession, db_obj: Unit) -> None:
    await session.delete(db_obj)
    await session.commit()
