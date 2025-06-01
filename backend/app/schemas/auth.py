"""Authentication-related Pydantic schemas."""

from pydantic import EmailStr, Field
from .base import BaseSchema


class Token(BaseSchema):
    access_token: str
    token_type: str = Field(default="bearer", const=True)


class LoginRequest(BaseSchema):
    email: EmailStr
    password: str
