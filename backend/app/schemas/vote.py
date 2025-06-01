"""Pydantic schemas for Vote domain objects."""

from __future__ import annotations
from datetime import datetime # Import datetime
from pydantic import Field # BaseModel is no longer needed directly
from .base import BaseSchema


class VoteBase(BaseSchema):
    proposal_id: str = Field(..., example="proposal-uuid")
    user_id: str = Field(..., example="user-uuid")
    choice: str = Field(..., example="yes")


class VoteCreate(VoteBase):
    pass


class VoteRead(VoteBase):
    id: str
    created_at: datetime # Changed to datetime

    # Config class is no longer needed, from_attributes=True is inherited from BaseSchema