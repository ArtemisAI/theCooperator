"""Celery background tasks for notifications and score recomputation."""

import asyncio # Required for running async code in sync Celery tasks if needed
from app.jobs.celery import celery_app
from app.core.logging import get_logger # Using the structured logger
from app.jobs.db_utils import get_db_session_for_task
from app.crud import task as task_crud
from app.crud import vote as vote_crud
from app.crud import score_entry as score_entry_crud
from app.crud import user as user_crud
from app.schemas.score_entry import ScoreEntryCreate
from app.core.exceptions import NotFoundException


logger = get_logger(__name__)

@celery_app.task
def send_notification_email(recipient_email: str, subject: str, body: str) -> None:
    """
    Simulates sending a notification email.
    Logs the email details using the structured logger.
    """
    logger.info(
        "Simulating email sending",
        recipient_email=recipient_email,
        subject=subject,
        body_length=len(body) # Avoid logging potentially large/sensitive body
    )
    # In a real scenario, this would integrate with an email client/service.
    # For example:
    # email_client.send(to=recipient_email, subject=subject, html_body=body)
    return f"Email simulation for {recipient_email} successful."


async def _recompute_scores_async(user_id: str):
    """Async helper for recompute_scores task."""
    async for session in get_db_session_for_task():
        db_user = await user_crud.get_user(session, user_id=user_id)
        if not db_user:
            logger.error("User not found for score recomputation", user_id=user_id)
            # Or raise NotFoundException - though this might make Celery retry indefinitely
            # depending on Celery error handling configuration for this task.
            # For now, just logging and exiting for this user.
            return f"User {user_id} not found."

        # Fetch user's completed tasks
        # Assuming task_crud.list_tasks can be filtered by assignee_id and status
        # This part needs actual implementation in task_crud or more specific methods
        # For now, let's imagine a method:
        # completed_tasks = await task_crud.get_completed_tasks_by_user(session, user_id=user_id)
        # num_completed_tasks = len(completed_tasks)

        # Placeholder: Get all tasks assigned to user, assume all are completed for simplicity
        user_tasks = await task_crud.list_tasks(session, offset=0, limit=1000) # Needs filtering
        num_completed_tasks = 0
        for task_item in user_tasks:
            if task_item.assignee_id == user_id and task_item.status == "done": # Assuming TaskStatus.done
                num_completed_tasks += 1

        # Fetch user's votes
        # Assuming vote_crud.list_votes_by_user exists or similar
        # For now, let's imagine a method:
        # user_votes = await vote_crud.get_votes_by_user(session, user_id=user_id)
        # num_votes = len(user_votes)

        # Placeholder: Count all votes by this user (needs new CRUD method: get_votes_by_user_id)
        # For now, let's use a placeholder value or skip if no direct method
        # Example: votes = await vote_crud.get_votes_by_user_id(session, user_id=user_id)
        # num_votes = len(votes)
        num_votes = 0 # Placeholder, as vote_crud doesn't have get_votes_by_user_id yet

        # Calculate score
        new_score = (num_completed_tasks * 10) + (num_votes * 5)

        # Create or update ScoreEntry
        # Check if a score entry exists, then update, else create.
        # For simplicity, this example creates a new one each time.
        # A more robust version would use score_entry_crud.get_by_user_and_update_or_create
        score_entry_obj = ScoreEntryCreate(user_id=user_id, score=new_score)
        await score_entry_crud.create_score_entry(session=session, obj_in=score_entry_obj)

        logger.info("Recomputed score for user", user_id=user_id, new_score=new_score, completed_tasks=num_completed_tasks, votes_participated=num_votes)
        return f"Score recomputed for user {user_id}: {new_score}"

@celery_app.task(name="recompute_user_scores") # Explicit name for clarity
def recompute_scores(user_id: str) -> str:
    """
    Synchronous Celery task wrapper for recomputing a user's participation score.
    Runs the actual async logic using asyncio.run().
    """
    # Celery tasks are typically synchronous. To call async code, use asyncio.run()
    # This is a common pattern for integrating async DB operations with Celery.
    # Ensure the Celery worker environment can handle this (e.g., not gevent with monkeypatching issues).
    # The default 'solo' pool for local dev in roadmap should be fine.
    logger.info(f"Received task to recompute scores for user_id: {user_id}")
    try:
        result = asyncio.run(_recompute_scores_async(user_id))
        return result
    except Exception as e:
        logger.error(f"Error in recompute_scores for user {user_id}: {e}", exc_info=True)
        # Depending on task configuration, this might lead to retries.
        # Re-raise to let Celery handle it based on its config (e.g., acks, retries).
        raise

# Example of a periodic task (if you had Celery Beat configured)
# @celery_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#    sender.add_periodic_task(
#        crontab(hour=0, minute=0), # Run daily at midnight
#        recompute_all_users_scores.s(),
#        name='recompute all user scores daily'
#    )

# @celery_app.task
# async def recompute_all_users_scores():
#    async for session in get_db_session_for_task():
#        users = await user_crud.list_users(session, limit=10000) # Adjust limit as needed
#        for user in users:
#            # Call the single user recompute, or batch operations
#            # Consider triggering individual tasks to avoid one massive task:
#            # recompute_scores.delay(user.id)
#            # For now, direct call (can be long for many users)
#            await _recompute_scores_async(user.id) # Assuming _recompute_scores_async is made callable
#     logger.info("Finished recomputing all user scores.")
#     return "All user scores recomputation process completed."