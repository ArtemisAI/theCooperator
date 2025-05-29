"""Celery application configuration (placeholder)."""

from celery import Celery
from app.core.config import settings

# Initialize Celery app for background tasks
celery_app = Celery(
    "theCooperator",
    broker=settings.CELERY_BROKER_URL,
)

# TODO: configure task autodiscovery, result backend, and serializers