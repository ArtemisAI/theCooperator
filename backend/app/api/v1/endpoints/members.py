"""REST endpoints for managing **Member** entities.

Routes are mounted under `/api/v1/members`.
"""

from __future__ import annotations

from typing import List # Changed from Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import member as crud_member # Updated import
from app.db import get_async_session
from app.schemas.member import MemberCreate, MemberRead, MemberUpdate # Updated import

router = APIRouter(prefix="/members", tags=["members"]) # Updated prefix and tags


# ---------------------------------------------------------------------------
# Collection routes
# ---------------------------------------------------------------------------


@router.get("/", response_model=List[MemberRead], summary="List members") # Updated response_model
async def list_members( # Renamed function
    *,
    session: AsyncSession = Depends(get_async_session),
    limit: int = 100,
    offset: int = 0,
) -> List[MemberRead]: # Updated return type hint
    """Return all members.

    Pagination is done via *limit/offset* query-parameters for simplicity.
    """
    return await crud_member.list_members(session, offset=offset, limit=limit) # Updated CRUD call


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=MemberRead, # Updated response_model
    summary="Create member", # Updated summary
)
async def create_member( # Renamed function
    *,
    session: AsyncSession = Depends(get_async_session),
    member_in: MemberCreate, # Updated parameter name and type
) -> MemberRead: # Updated return type hint
    """Create new member and return it."""
    # The check for existing email can be handled by the database unique constraint
    # or within the CRUD create function if specific error handling is needed there.
    # For now, removing it here to simplify the API layer, assuming CRUD/DB handles it.
    # existing = await crud_member.get_member_by_email(session, member_in.email)
    # if existing:
    #     raise HTTPException(status_code=409, detail="E-mail already registered")
    return await crud_member.create_member(session, member_in) # Updated CRUD call


# ---------------------------------------------------------------------------
# Item routes (by id)
# ---------------------------------------------------------------------------


@router.get("/{member_id}", response_model=MemberRead, summary="Get member by id") # Updated path param
async def read_member( # Renamed function
    *,
    session: AsyncSession = Depends(get_async_session),
    member_id: str, # Updated parameter name
) -> MemberRead: # Updated return type hint
    db_member = await crud_member.get_member(session, member_id) # Updated CRUD call and var name
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found") # Updated detail message
    return db_member


@router.put("/{member_id}", response_model=MemberRead, summary="Update member") # Updated path param
async def update_member( # Renamed function
    *,
    session: AsyncSession = Depends(get_async_session),
    member_id: str, # Updated parameter name
    member_in: MemberUpdate, # Updated parameter name and type
) -> MemberRead: # Updated return type hint
    db_member = await crud_member.get_member(session, member_id) # Updated CRUD call and var name
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found") # Updated detail message

    return await crud_member.update_member(session, db_member, member_in) # Updated CRUD call


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete member") # Updated path param
async def delete_member( # Renamed function
    *,
    session: AsyncSession = Depends(get_async_session),
    member_id: str, # Updated parameter name
) -> None:
    db_member = await crud_member.get_member(session, member_id) # Updated CRUD call and var name
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found") # Updated detail message

    await crud_member.delete_member(session, db_member) # Updated CRUD call
