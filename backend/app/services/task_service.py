"""Business logic for Task operations."""

from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import task as task_crud
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import Task
from app.core.exceptions import AssignmentLimitExceededException, NotFoundException

MAX_ASSIGNED_TASKS_PER_USER = 3

async def create_task_with_assignment_check(
    db: AsyncSession, task_in: TaskCreate
) -> Task:
    """
    Creates a new task, checking assignment limits if an assignee is provided.
    """
    if task_in.assignee_id:
        assigned_count = await task_crud.count_tasks_by_assignee_id(
            db, task_in.assignee_id
        )
        if assigned_count >= MAX_ASSIGNED_TASKS_PER_USER:
            raise AssignmentLimitExceededException(
                f"User {task_in.assignee_id} has reached the maximum task assignment limit of {MAX_ASSIGNED_TASKS_PER_USER}."
            )

    new_task = await task_crud.create_task(session=db, obj_in=task_in)
    return new_task

async def update_task_with_assignment_check(
    db: AsyncSession, task_id: str, task_in: TaskUpdate
) -> Task | None:
    """
    Updates a task. If the assignee is changed or added,
    checks the new assignee's task limits.
    """
    db_task = await task_crud.get_task(session=db, task_id=task_id)
    if not db_task:
        # Or raise NotFoundException, depending on desired behavior at API level
        return None

    # Check limits only if assignee_id is being set/changed in the update
    # and it's different from the current assignee or current assignee is None
    if task_in.assignee_id and task_in.assignee_id != db_task.assignee_id:
        assigned_count = await task_crud.count_tasks_by_assignee_id(
            db, task_in.assignee_id
        )
        if assigned_count >= MAX_ASSIGNED_TASKS_PER_USER:
            raise AssignmentLimitExceededException(
                f"User {task_in.assignee_id} has reached the maximum task assignment limit of {MAX_ASSIGNED_TASKS_PER_USER}."
            )

    updated_task = await task_crud.update_task(session=db, db_obj=db_task, obj_in=task_in)
    return updated_task

# Placeholder for other functions if needed
def compute_task_overview() -> None:
    """Compute summary statistics for tasks (e.g., counts by status)."""
    # TODO: aggregate task data for dashboard
    pass