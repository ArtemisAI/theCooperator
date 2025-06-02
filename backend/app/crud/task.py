"""Async CRUD helpers for the Task model."""

from __future__ import annotations
from typing import Sequence
from sqlalchemy import select, func # Added func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task, TaskStatus # Added TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


async def get_task(session: AsyncSession, task_id: str) -> Task | None:
    """Return a Task by id or None."""
    result = await session.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def list_tasks(
    session: AsyncSession,
    *,
    offset: int = 0,
    limit: int = 100,
) -> Sequence[Task]:
    """Return a slice of tasks ordered by creation date."""
    result = await session.execute(select(Task).offset(offset).limit(limit))
    return result.scalars().all()


async def count_active_tasks_by_assignee(session: AsyncSession, assignee_id: str) -> int:
    """Count active (non-done) tasks assigned to a specific user."""
    count_query = (
        select(func.count())
        .select_from(Task)
        .where(Task.assignee_id == assignee_id)
        .where(Task.status != TaskStatus.done)
    )
    result = await session.execute(count_query)
    count = result.scalar_one()
    return count if count is not None else 0


async def create_task(session: AsyncSession, obj_in: TaskCreate) -> Task:
    """Create a new Task object."""
    db_obj = Task(
        title=obj_in.title,
        description=obj_in.description,
        status=obj_in.status,
        due_date=obj_in.due_date,
        assignee_id=obj_in.assignee_id,
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_task(
    session: AsyncSession,
    db_obj: Task,
    obj_in: TaskUpdate,
) -> Task:
    """Update existing Task fields."""
    if obj_in.title is not None:
        db_obj.title = obj_in.title
    if obj_in.description is not None:
        db_obj.description = obj_in.description
    if obj_in.status is not None:
        db_obj.status = obj_in.status
    if obj_in.due_date is not None:
        db_obj.due_date = obj_in.due_date
    if obj_in.assignee_id is not None:
        db_obj.assignee_id = obj_in.assignee_id
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def delete_task(session: AsyncSession, db_obj: Task) -> None:
    """Delete a Task object."""
    await session.delete(db_obj)
    await session.commit()