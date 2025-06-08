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


class TaskBase(BaseModel):
    title: str
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None  # ISO format
    assignee_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
