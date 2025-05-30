"""Pydantic schemas for the *Member* domain object.

These data-transfer objects (DTOs) are used by the API layer and tests. We keep
them separate from SQLAlchemy models so that the database layer remains
decoupled from FastAPI request/response validation.
"""

from __future__ import annotations
from datetime import date
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field

from app.models.member import MemberSex, MemberType # Updated import path


class MemberBase(BaseModel):
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    first_name: str = Field(..., examples=["John"])
    last_name: str = Field(..., examples=["Doe"])
    legacy_full_name: Optional[str] = Field(None, examples=["John Doe"])
    dob: Optional[date] = Field(None, examples=["1990-01-01"])
    phone_number: Optional[str] = Field(None, examples=["555-1234"])
    occupation: Optional[str] = Field(None, examples=["Software Developer"])
    sex: Optional[MemberSex] = Field(None, examples=[MemberSex.male])
    skills: Optional[List[str]] = Field(None, examples=[["python", "fastapi"]])
    education_level: Optional[str] = Field(None, examples=["Bachelor's Degree"])
    member_type: MemberType = Field(..., examples=[MemberType.primary])
    unit_id: Optional[str] = Field(None, examples=["uuid-of-unit"]) # UUIDs are strings

    class Config:
        use_enum_values = True


class MemberCreate(MemberBase):
    # Password is not part of MemberCreate anymore as per instructions
    pass


class MemberUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    legacy_full_name: Optional[str] = None
    dob: Optional[date] = None
    phone_number: Optional[str] = None
    occupation: Optional[str] = None
    sex: Optional[MemberSex] = None
    skills: Optional[List[str]] = None
    education_level: Optional[str] = None
    member_type: Optional[MemberType] = None
    unit_id: Optional[str] = None

    class Config:
        use_enum_values = True


class MemberRead(MemberBase):
    id: str
    unit_label: Optional[str] = None # To be populated by joining in CRUD

    # Fields from MemberBase are inherited:
    # email, first_name, last_name, legacy_full_name, dob, phone_number,
    # occupation, sex, skills, education_level, member_type, unit_id

    class Config:
        orm_mode = True # Pydantic V1
        # from_attributes = True # Pydantic V2
        use_enum_values = True


# This schema is for use in UnitRead to avoid circular dependencies.
class MemberReadWithoutUnit(MemberBase):
    id: str
    # Inherits fields from MemberBase:
    # email, first_name, last_name, legacy_full_name, dob, phone_number,
    # occupation, sex, skills, education_level, member_type
    # Explicitly does NOT include unit_id or unit_label to prevent recursion if this schema were to include Unit data

    class Config:
        orm_mode = True # Pydantic V1
        # from_attributes = True # Pydantic V2
        use_enum_values = True
