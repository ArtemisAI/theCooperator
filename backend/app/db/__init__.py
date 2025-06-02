"""Database helpers (async SQLAlchemy engine, session factories, dependencies).

This file centralises all DB-related primitives so other modules can simply do:

    from app.db import async_session, get_async_session

The engine uses **asyncpg**; the sync variant (`config.settings.DSN_SYNC`) is
meant for offline tooling such as Alembic migrations.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# ---------------------------------------------------------------------------
# Engine & session factory
# ---------------------------------------------------------------------------

engine = create_async_engine(settings.DSN_ASYNC, echo=False, future=True)

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an **AsyncSession** bound to a transaction.

    Usage:
        @router.get("/members")
        async def list_members(session: AsyncSession = Depends(get_async_session)):
            ...
    """

    async with async_session() as session:  # noqa: WPS501 – context manager OK
        yield session
