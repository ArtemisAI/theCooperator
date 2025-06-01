"""Celery application configuration (placeholder)."""

from celery import Celery
from app.core.config import settings

# Initialize Celery app for background tasks
celery_app = Celery(
    "theCooperator",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL, # Using Redis as result backend too for simplicity
    # Alternatively, use a different backend like database if preferred
)

# Configuration options
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Autodiscover tasks from 'app.jobs.tasks'
    # This will look for a tasks.py file in the app.jobs package
    include=['app.jobs.tasks']
)

# Optional: If you want to use a custom Task base class for logging or other features
# class BaseTaskWithLogging(celery_app.Task):
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         logger.error(f'Task {task_id} failed: {exc}', exc_info=einfo)
#         super().on_failure(exc, task_id, args, kwargs, einfo)

# celery_app.Task = BaseTaskWithLogging

# Optional: Autodiscover tasks (alternative to `include` but `include` is more explicit)
# celery_app.autodiscover_tasks(['app.jobs']) # Looks for tasks.py in specified packages