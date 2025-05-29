"""Pydantic schemas for Vote domain objects."""

from __future__ import annotations
from pydantic import BaseModel, Field


class VoteBase(BaseModel):
    proposal_id: str = Field(..., example="proposal-uuid")
    user_id: str = Field(..., example="user-uuid")
    choice: str = Field(..., example="yes")


class VoteCreate(VoteBase):
    pass


class VoteRead(VoteBase):
    id: str
    created_at: str | None  # ISO datetime string

    class Config:
        orm_mode = True