"""Pydantic schemas for ScoreEntry domain objects."""

from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field


class ScoreEntryBase(BaseModel):
    user_id: str = Field(..., example="user-uuid")
    score: int = Field(..., example=42)


class ScoreEntryCreate(ScoreEntryBase):
    pass


class ScoreEntryRead(ScoreEntryBase):
    id: str
    timestamp: datetime

    class Config:
        orm_mode = True