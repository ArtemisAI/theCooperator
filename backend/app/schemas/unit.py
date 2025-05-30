"""Pydantic schemas for the **Unit** domain object."""

from __future__ import annotations
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.unit import UnitStatus # Assuming UnitStatus is in app.models.unit
# This import will cause an error until MemberReadWithoutUnit is created.
# For now, we'll add it as requested.
from .member import MemberReadWithoutUnit


class UnitBase(BaseModel):
    label: str = Field(..., examples=["Unit 2B"]) # This field might be deprecated by unit_number
    unit_number: str = Field(..., examples=["Unit 101"])
    status: UnitStatus = Field(default=UnitStatus.active, examples=[UnitStatus.active])

    class Config:
        use_enum_values = True # Important for enums


class UnitCreate(UnitBase):
    pass


class UnitUpdate(BaseModel):
    label: Optional[str] = None # Kept for now, but might be deprecated
    unit_number: Optional[str] = None
    status: Optional[UnitStatus] = None

    class Config:
        use_enum_values = True # Important for enums


class UnitRead(UnitBase):
    id: str
    # unit_number is already in UnitBase
    # status is already in UnitBase
    members: List[MemberReadWithoutUnit] = []

    class Config:
        orm_mode = True
        use_enum_values = True # Ensure enums are handled correctly
