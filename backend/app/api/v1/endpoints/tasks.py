"""CRUD endpoints for Task objects."""

from __future__ import annotations

from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.task import list_tasks, get_task, create_task, update_task as crud_update_task, delete_task # Renamed update_task
from app.db import get_async_session
from app.schemas.task import TaskRead, TaskCreate, TaskUpdate
from app.services.task_service import TaskService # Added TaskService
from app.core.error_handlers import NotFoundException # Added NotFoundException

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
    task_in: TaskCreate, # Moved task_in before session
    session: AsyncSession = Depends(get_async_session),
) -> TaskRead:
    return await create_task(session, task_in)

@router.get("/{task_id}", response_model=TaskRead, summary="Get task by id")
async def read_task(
    task_id: str, # Moved task_id before session
    session: AsyncSession = Depends(get_async_session),
) -> TaskRead:
    db_task = await get_task(session, task_id) # Renamed db_obj to db_task
    if not db_task:
        # Using NotFoundException which should be handled by our global handler
        raise NotFoundException(detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=TaskRead, summary="Update task")
async def modify_task(
    task_id: str, # Moved path param first
    task_in: TaskUpdate, # Moved body param second
    session: AsyncSession = Depends(get_async_session), # Depends last
) -> TaskRead:
    task_service = TaskService(session)
    db_task = await get_task(session, task_id)
    if not db_task:
        raise NotFoundException(detail="Task not found")

    # Handle assignee changes first using the service
    assignee_updated_by_service = False
    if "assignee_id" in task_in.dict(exclude_unset=True): # Check if assignee_id was explicitly provided
        if task_in.assignee_id is not None:
            if task_in.assignee_id != db_task.assignee_id:
                # Assign to a new user or change assignee
                db_task = await task_service.assign_task_to_user(task_id=task_id, user_id=task_in.assignee_id)
                assignee_updated_by_service = True
        else: # task_in.assignee_id is None, meaning unassign
            if db_task.assignee_id is not None:
                db_task = await task_service.unassign_task(task_id=task_id)
                assignee_updated_by_service = True

    # Handle other field updates
    # If assignee was updated by service, the service already committed changes.
    # We only need to process other fields if they exist.
    other_updates_dict = task_in.dict(exclude_unset=True)
    if assignee_updated_by_service:
        other_updates_dict.pop("assignee_id", None) # Remove assignee_id if it was handled

    if other_updates_dict: # If there are other fields to update
        # Create a new TaskUpdate schema instance for other fields
        # Note: Pydantic models are immutable by default, but creating a new one is fine.
        # Or, we can pass the dict directly if crud_update_task supports it,
        # but it's safer to pass a schema instance.
        # However, crud_update_task expects TaskUpdate, which might include assignee_id.
        # The crud_update_task should ideally ignore fields that are None in the schema.
        # Let's create a new TaskUpdate schema ensuring only intended fields are passed.

        # If assignee_id was handled, we don't want crud_update_task to process it again.
        # The current db_task object is already updated by the service if assignee changed.
        # So, we pass the potentially modified db_task to crud_update_task.

        # We need to ensure that crud_update_task doesn't revert the assignee_id change
        # if task_in originally contained assignee_id.
        # The `obj_in` for crud_update_task should not contain assignee_id if it was handled by service.

        update_schema_for_crud = TaskUpdate(**other_updates_dict)
        db_task = await crud_update_task(session, db_obj=db_task, obj_in=update_schema_for_crud)

    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete task")
async def remove_task(
    task_id: str, # Moved path param first
    session: AsyncSession = Depends(get_async_session), # Depends last
): # Removed -> None
    db_task = await get_task(session, task_id) # Renamed
    if not db_task:
        raise NotFoundException(detail="Task not found") # Using custom exception
    await delete_task(session, db_task)