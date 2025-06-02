"""Authentication-related Pydantic schemas."""

from typing import Literal # Added Literal
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = Field(default="bearer") # Changed to use Literal


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
