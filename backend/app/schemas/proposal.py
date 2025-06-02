"""Pydantic schemas for Proposal domain objects."""

from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field


class ProposalBase(BaseModel):
    title: str = Field(..., example="Approve new budget")
    description: str | None = Field(None, example="Yearly spending plan for maintenance")


class ProposalCreate(ProposalBase):
    pass


class ProposalUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class ProposalRead(ProposalBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True