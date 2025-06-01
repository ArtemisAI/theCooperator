"""Pydantic schemas for Task domain objects."""

from __future__ import annotations

from datetime import date
from pydantic import Field # BaseModel is no longer needed directly
from app.models.task import TaskStatus # Make sure TaskStatus is imported correctly
from .base import BaseSchema


class TaskBase(BaseSchema):
    title: str = Field(..., example="Fix broken door")
    description: str | None = Field(None, example="Lubricate hinges and tighten screws")
    status: TaskStatus = Field(default=TaskStatus.todo)
    due_date: date | None = Field(None, example="2024-12-31")
    assignee_id: str | None = Field(None, example="user-uuid")

    model_config = {
        "use_enum_values": True,
        # from_attributes is inherited from BaseSchema
    }


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseSchema): # Inherit from BaseSchema
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    due_date: date | None = None
    assignee_id: str | None = None

    model_config = {
        "use_enum_values": True,
        # from_attributes is inherited from BaseSchema
    }


class TaskRead(TaskBase):
    id: str

    # from_attributes is inherited, use_enum_values is needed for status
    model_config = {
        "use_enum_values": True,
    }