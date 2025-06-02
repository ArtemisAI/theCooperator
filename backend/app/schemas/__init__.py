"""Pydantic schemas for request/response bodies.

Will be expanded in Phase 1. For the scaffolding step we only add a `User` and
`Token` example to demonstrate FastAPI docs generation.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
