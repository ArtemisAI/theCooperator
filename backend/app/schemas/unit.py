"""Pydantic schemas for the **Unit** domain object."""

from __future__ import annotations

from pydantic import BaseModel, Field


class UnitBase(BaseModel):
    label: str = Field(..., examples=["Unit 2B"])


class UnitCreate(UnitBase):
    pass


class UnitUpdate(BaseModel):
    label: str | None = None


class UnitRead(UnitBase):
    id: str

    class Config:
        orm_mode = True
