"""Async CRUD helpers for the Vote model (placeholder)."""

from __future__ import annotations
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

# TODO: implement actual import and CRUD operations
from app.models.vote import Vote
from app.schemas.vote import VoteCreate


async def list_votes(
    session: AsyncSession,
    *,
    offset: int = 0,
    limit: int = 100,
) -> Sequence[Vote]:
    """Return a slice of votes."""
    # TODO: execute select query
    raise NotImplementedError


async def create_vote(
    session: AsyncSession,
    obj_in: VoteCreate,
) -> Vote:
    """Record a new vote."""
    # TODO: insert and commit Vote
    raise NotImplementedError