"""CRUD endpoints for **Unit** objects."""

from __future__ import annotations

from typing import List # Changed from Sequence for consistency with List[schemas.UnitRead]
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import unit as crud_unit
from app.db import get_async_session
from app.schemas.unit import UnitCreate, UnitRead, UnitUpdate

router = APIRouter(prefix="/units", tags=["units"])


@router.get("/", response_model=List[UnitRead], summary="List units") # Changed to List
async def list_units(
    *,
    session: AsyncSession = Depends(get_async_session),
    limit: int = 100,
    offset: int = 0,
) -> List[UnitRead]: # Changed to List
    return await crud_unit.list_units(session, offset=offset, limit=limit)


@router.post("/", status_code=201, response_model=UnitRead, summary="Create unit")
async def create_unit(
    *,
    session: AsyncSession = Depends(get_async_session),
    unit_in: UnitCreate,
) -> UnitRead:
    return await crud_unit.create_unit(session, unit_in)


@router.get("/{unit_id}", response_model=UnitRead, summary="Get unit by id")
async def read_unit(
    *,
    session: AsyncSession = Depends(get_async_session),
    unit_id: str,
) -> UnitRead:
    db_unit = await crud_unit.get_unit(session, unit_id)
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return db_unit


@router.put("/{unit_id}", response_model=UnitRead, summary="Update unit")
async def update_unit(
    *,
    session: AsyncSession = Depends(get_async_session),
    unit_id: str,
    unit_in: UnitUpdate,
) -> UnitRead:
    db_unit = await crud_unit.get_unit(session, unit_id)
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return await crud_unit.update_unit(session, db_unit, unit_in)


@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete unit")
async def delete_unit(
    *,
    session: AsyncSession = Depends(get_async_session),
    unit_id: str,
) -> None:
    db_unit = await crud_unit.get_unit(session, unit_id)
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    await crud_unit.delete_unit(session, db_unit)
