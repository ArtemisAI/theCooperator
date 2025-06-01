"""Pydantic schemas for the **Unit** domain object."""

from __future__ import annotations

from pydantic import Field # BaseModel is no longer needed directly
from .base import BaseSchema


class UnitBase(BaseSchema):
    label: str = Field(..., examples=["Unit 2B"])


class UnitCreate(UnitBase):
    pass


class UnitUpdate(BaseSchema): # Inherit from BaseSchema
    label: str | None = None


class UnitRead(UnitBase):
    id: str

    # Config class is no longer needed, from_attributes=True is inherited from BaseSchema
