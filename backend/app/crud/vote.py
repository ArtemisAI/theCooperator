"""Async CRUD helpers for the Vote model."""

from __future__ import annotations
from typing import Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vote import Vote
from app.schemas.vote import VoteCreate


async def get_vote(session: AsyncSession, vote_id: str) -> Vote | None:
    """Return a Vote by id or None."""
    result = await session.execute(select(Vote).where(Vote.id == vote_id))
    return result.scalar_one_or_none()

async def list_votes_for_proposal(
    session: AsyncSession,
    proposal_id: str,
    offset: int = 0,
    limit: int = 1000, # Default to a high limit for all votes on a proposal
) -> Sequence[Vote]:
    """Return a slice of votes for a specific proposal."""
    result = await session.execute(
        select(Vote)
        .where(Vote.proposal_id == proposal_id)
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()

async def get_votes_count_for_proposal(session: AsyncSession, proposal_id: str) -> int:
    """Count the number of votes cast for a specific proposal."""
    result = await session.execute(
        select(func.count(Vote.id)).where(Vote.proposal_id == proposal_id)
    )
    return result.scalar_one()

async def create_vote(session: AsyncSession, obj_in: VoteCreate) -> Vote:
    """Record a new vote."""
    # Basic validation: ensure user hasn't voted on this proposal yet might be here or service layer
    # For now, CRUD is simple.
    db_obj = Vote(
        proposal_id=obj_in.proposal_id,
        user_id=obj_in.user_id,
        choice=obj_in.choice,
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj

async def delete_vote(session: AsyncSession, db_obj: Vote) -> None:
    """Delete a Vote object."""
    await session.delete(db_obj)
    await session.commit()