"""CRUD endpoints for Task objects."""

from __future__ import annotations

from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.task import list_tasks, get_task, create_task, update_task, delete_task
from app.db import get_async_session
from app.schemas.task import TaskRead, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskRead], summary="List tasks")
async def read_tasks(
    session: AsyncSession = Depends(get_async_session),
    limit: int = 100,
    offset: int = 0,
) -> Sequence[TaskRead]:
    return await list_tasks(session, offset=offset, limit=limit)

@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create task",
)
async def create_new_task(
    session: AsyncSession = Depends(get_async_session),
    task_in: TaskCreate,
) -> TaskRead:
    return await create_task(session, task_in)

@router.get("/{task_id}", response_model=TaskRead, summary="Get task by id")
async def read_task(
    session: AsyncSession = Depends(get_async_session),
    task_id: str,
) -> TaskRead:
    db_obj = await get_task(session, task_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_obj

@router.put("/{task_id}", response_model=TaskRead, summary="Update task")
async def modify_task(
    session: AsyncSession = Depends(get_async_session),
    task_id: str,
    task_in: TaskUpdate,
) -> TaskRead:
    db_obj = await get_task(session, task_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return await update_task(session, db_obj, task_in)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete task")
async def remove_task(
    session: AsyncSession = Depends(get_async_session),
    task_id: str,
) -> None:
    db_obj = await get_task(session, task_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await delete_task(session, db_obj)