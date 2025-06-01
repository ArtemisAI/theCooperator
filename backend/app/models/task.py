"""Task model stub.

A Kanban-style task assigned to member(s) or unit(s).
"""

from uuid import uuid4
import enum # Import Python's enum module

from sqlalchemy import Column, Date, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Enum as SAEnum # Import SQLAlchemy's Enum explicitly

from app.models import Base


class TaskStatus(str, enum.Enum): # Inherit from enum.Enum
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SAEnum(TaskStatus), default=TaskStatus.todo, nullable=False) # Use SAEnum
    due_date = Column(Date, nullable=True)
    assignee_id = Column(String, ForeignKey("users.id"), nullable=True)

    # Relationships
    assignee = relationship("User", back_populates="tasks")
