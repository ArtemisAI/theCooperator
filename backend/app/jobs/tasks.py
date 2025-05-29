"""Celery background tasks for notifications and score recomputation."""

from app.jobs.celery import celery_app

@celery_app.task
def send_notification_email(user_id: str, subject: str, body: str) -> None:
    """Send notification email to a user (placeholder)."""
    # TODO: integrate with email service (SMTP, SendGrid, etc.)
    pass

@celery_app.task
def recompute_scores() -> None:
    """Periodic task to recompute participation scores."""
    # TODO: call metric_service.recompute_scorecards
    pass