from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task, TaskStatus
from app.crud.task import count_active_tasks_by_assignee, get_task, update_task
from app.core.config import settings
from app.core.error_handlers import BadRequestException, NotFoundException
from app.schemas.task import TaskUpdate

class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def assign_task_to_user(self, task_id: str, user_id: str) -> Task:
        """
        Assigns a task to a user, enforcing task assignment limits.
        """
        task = await get_task(self.session, task_id)
        if not task:
            raise NotFoundException(f"Task with id {task_id} not found.")

        # Check if task is already completed
        if task.status == TaskStatus.done:
            raise BadRequestException("Cannot assign a completed task.")

        # If task is already assigned to this user, no action needed
        if task.assignee_id == user_id:
            return task

        # Check assignment limit for the target user
        active_task_count = await count_active_tasks_by_assignee(self.session, user_id)
        if active_task_count >= settings.MAX_TASKS_PER_USER:
            raise BadRequestException(
                f"User has reached the maximum number of assigned tasks ({settings.MAX_TASKS_PER_USER})."
            )

        # Assign the task
        task_update_schema = TaskUpdate(assignee_id=user_id)
        updated_task = await update_task(self.session, db_obj=task, obj_in=task_update_schema)
        return updated_task

    async def unassign_task(self, task_id: str) -> Task:
        """
        Unassigns a task from its current assignee.
        """
        task = await get_task(self.session, task_id)
        if not task:
            raise NotFoundException(f"Task with id {task_id} not found.")

        if task.assignee_id is None:
            # Task is not assigned, nothing to do
            return task

        # Check if task is already completed
        if task.status == TaskStatus.done:
            raise BadRequestException("Cannot unassign a completed task.")

        task_update_schema = TaskUpdate(assignee_id=None) # Assuming None means unassigned
        updated_task = await update_task(self.session, db_obj=task, obj_in=task_update_schema)
        return updated_task