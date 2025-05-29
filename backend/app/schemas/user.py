"""Pydantic schemas for the *User* domain object.

These data-transfer objects (DTOs) are used by the API layer and tests. We keep
them separate from SQLAlchemy models so that the database layer remains
decoupled from FastAPI request/response validation.
"""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr = Field(..., examples=["alice@example.com"])
    full_name: str | None = Field(None, examples=["Alice Example"])
    role: UserRole = Field(default=UserRole.resident)

    class Config:
        use_enum_values = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None

    class Config:
        use_enum_values = True


class UserRead(UserBase):
    id: str

    class Config:
        orm_mode = True
