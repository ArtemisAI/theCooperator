"""Authentication-related Pydantic schemas."""

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer", const=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
