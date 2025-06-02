"""Task model stub.

A Kanban-style task assigned to member(s) or unit(s).
"""

import enum # Standard library enum
from uuid import uuid4

from sqlalchemy import Column, Date, Enum as SqlAlchemyEnum, ForeignKey, String, Text # Renamed Enum

from app.models import Base


class TaskStatus(str, enum.Enum): # Inherit from str and enum.Enum
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SqlAlchemyEnum(TaskStatus), default=TaskStatus.todo, nullable=False) # Use aliased SqlAlchemyEnum
    due_date = Column(Date, nullable=True)
    assignee_id = Column(String, ForeignKey("users.id"), nullable=True)
