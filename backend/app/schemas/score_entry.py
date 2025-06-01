"""Pydantic schemas for ScoreEntry domain objects."""

from __future__ import annotations
from datetime import datetime
from pydantic import Field # BaseModel is no longer needed directly
from .base import BaseSchema


class ScoreEntryBase(BaseSchema):
    user_id: str = Field(..., example="user-uuid")
    score: int = Field(..., example=42)


class ScoreEntryCreate(ScoreEntryBase):
    pass


class ScoreEntryRead(ScoreEntryBase):
    id: str
    timestamp: datetime

    # Config class is no longer needed, from_attributes=True is inherited from BaseSchema