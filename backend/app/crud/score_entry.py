"""Async CRUD helpers for the ScoreEntry model (placeholder)."""

from __future__ import annotations
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

# TODO: implement actual import and CRUD operations
from app.models.score_entry import ScoreEntry
from app.schemas.score_entry import ScoreEntryCreate


async def list_score_entries(
    session: AsyncSession,
    *,
    offset: int = 0,
    limit: int = 100,
) -> Sequence[ScoreEntry]:
    """Return a slice of score entries."""
    # TODO: execute select query
    raise NotImplementedError


async def create_score_entry(
    session: AsyncSession,
    obj_in: ScoreEntryCreate,
) -> ScoreEntry:
    """Insert a new ScoreEntry."""
    # TODO: insert and commit ScoreEntry
    raise NotImplementedError