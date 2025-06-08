from celery import Celery

celery_app = Celery(
    'thecooperator', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0'
)

@celery_app.task
def send_due_date_reminder(task_id: int):
    # placeholder for email reminder logic
    print(f"Reminder: task {task_id} is due soon")
