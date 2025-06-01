from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import async_session # This is the async_sessionmaker

async def get_db_session_for_task() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields an SQLAlchemy AsyncSession for use in Celery tasks.
    Ensures the session is properly closed.
    """
    async with async_session() as session:
        try:
            yield session
            # Only commit if the task itself hasn't explicitly committed or rolled back
            # For simplicity, tasks should manage their own commits/rollbacks.
            # If a task raises an exception, the session will be rolled back by the context manager.
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close() # Though context manager should handle this.
