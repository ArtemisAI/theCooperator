"""Pydantic schemas for Task domain objects."""

from __future__ import annotations

from datetime import date
from pydantic import BaseModel, Field
from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., example="Fix broken door")
    description: str | None = Field(None, example="Lubricate hinges and tighten screws")
    status: TaskStatus = Field(default=TaskStatus.todo)
    due_date: date | None = Field(None, example="2024-12-31")
    assignee_id: str | None = Field(None, example="user-uuid")

    class Config:
        use_enum_values = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    due_date: date | None = None
    assignee_id: str | None = None

    class Config:
        use_enum_values = True


class TaskRead(TaskBase):
    id: str

    class Config:
        orm_mode = True