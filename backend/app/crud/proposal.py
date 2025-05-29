"""Async CRUD helpers for the Proposal model (placeholder)."""

from __future__ import annotations
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

# TODO: implement actual import and CRUD operations
from app.models.proposal import Proposal
from app.schemas.proposal import ProposalCreate, ProposalUpdate


async def get_proposal(session: AsyncSession, proposal_id: str) -> Proposal | None:
    """Return a Proposal by id or None."""
    # TODO: execute select query
    raise NotImplementedError


async def list_proposals(
    session: AsyncSession,
    *,
    offset: int = 0,
    limit: int = 100,
) -> Sequence[Proposal]:
    """Return a slice of proposals."""
    # TODO: execute select query
    raise NotImplementedError


async def create_proposal(
    session: AsyncSession,
    obj_in: ProposalCreate,
) -> Proposal:
    """Create a new Proposal object."""
    # TODO: insert and commit Proposal
    raise NotImplementedError


async def update_proposal(
    session: AsyncSession,
    db_obj: Proposal,
    obj_in: ProposalUpdate,
) -> Proposal:
    """Update existing Proposal fields."""
    # TODO: update fields, commit, and refresh
    raise NotImplementedError


async def delete_proposal(session: AsyncSession, db_obj: Proposal) -> None:
    """Delete a Proposal object."""
    # TODO: delete and commit
    raise NotImplementedError