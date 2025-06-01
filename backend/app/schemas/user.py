"""Pydantic schemas for the *User* domain object.

These data-transfer objects (DTOs) are used by the API layer and tests. We keep
them separate from SQLAlchemy models so that the database layer remains
decoupled from FastAPI request/response validation.
"""

from __future__ import annotations

from pydantic import EmailStr, Field # BaseModel is no longer needed directly
from app.models.user import UserRole # Ensure UserRole is imported
from .base import BaseSchema


class UserBase(BaseSchema):
    email: EmailStr = Field(..., examples=["alice@example.com"])
    full_name: str | None = Field(None, examples=["Alice Example"])
    role: UserRole = Field(default=UserRole.resident)

    model_config = {
        "use_enum_values": True,
        # from_attributes is inherited
    }


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseSchema): # Inherit from BaseSchema
    full_name: str | None = None
    role: UserRole | None = None

    model_config = {
        "use_enum_values": True,
        # from_attributes is inherited
    }


class UserRead(UserBase):
    id: str

    # from_attributes is inherited, use_enum_values is needed for role
    model_config = {
        "use_enum_values": True,
    }
