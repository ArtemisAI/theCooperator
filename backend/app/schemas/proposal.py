"""Pydantic schemas for Proposal domain objects."""

from __future__ import annotations
from datetime import datetime
from pydantic import Field # BaseModel is no longer needed directly
from .base import BaseSchema


class ProposalBase(BaseSchema):
    title: str = Field(..., example="Approve new budget")
    description: str | None = Field(None, example="Yearly spending plan for maintenance")


class ProposalCreate(ProposalBase):
    pass


class ProposalUpdate(BaseSchema): # Inherit from BaseSchema
    title: str | None = None
    description: str | None = None


class ProposalRead(ProposalBase):
    id: str
    created_at: datetime

    # Config class is no longer needed, from_attributes=True is inherited from BaseSchema