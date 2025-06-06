from pydantic import BaseModel
from typing import Optional

class UnitBase(BaseModel):
    name: str

class UnitCreate(UnitBase):
    pass

class Unit(UnitBase):
    id: int

    class Config:
        orm_mode = True

class MemberBase(BaseModel):
    name: str
    email: str
    unit_id: Optional[int] = None

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    id: int

    class Config:
        orm_mode = True
