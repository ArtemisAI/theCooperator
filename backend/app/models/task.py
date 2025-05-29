"""Task model stub.

A Kanban-style task assigned to member(s) or unit(s).
"""

from uuid import uuid4

from sqlalchemy import Column, Date, Enum, ForeignKey, String, Text

from app.models import Base


class TaskStatus(str, Enum):  # type: ignore[call-arg]
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo, nullable=False)
    due_date = Column(Date, nullable=True)
    assignee_id = Column(String, ForeignKey("users.id"), nullable=True)
