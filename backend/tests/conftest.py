"""Shared pytest fixtures for backend tests."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:  # noqa: D401
    """Create a dedicated event loop for the test session."""

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:  # noqa: D401 – pytest fixture.
    """Return *TestClient* backed by in-memory SQLite DB."""

    from app.main import create_app  # noqa: WPS433 – local import after patching
    from app.models import Base  # noqa: WPS433
    import app.db as db_module  # noqa: WPS433

    SQLITE_TEST_DSN = "sqlite+aiosqlite:///:memory:"
    # Set DATABASE_URL for settings to pick up SQLite DSN
    monkeypatch.setenv("DATABASE_URL", SQLITE_TEST_DSN)
    # Set other potentially conflicting PG env vars to something irrelevant or consistent with test DSN
    monkeypatch.setenv("POSTGRES_HOST", "")
    monkeypatch.setenv("POSTGRES_USER", "")
    monkeypatch.setenv("POSTGRES_PASSWORD", "")
    monkeypatch.setenv("POSTGRES_DB", "")


    from app.core.config import get_settings
    # Clear LRU cache for get_settings to ensure it re-reads DATABASE_URL
    get_settings.cache_clear()
    # This settings instance will be used when app.db imports it.
    # No need to explicitly pass test_specific_settings around if this works.
    _ = get_settings() # This call ensures settings are loaded with new env vars

    # Now, when app.db is imported (e.g. by create_app, or by db_module itself),
    # it should use the DATABASE_URL for its engine.

    # We still need an engine_test for creating tables and an override session
    # that is explicitly tied to this engine_test to be absolutely sure.
    engine_test = create_async_engine(SQLITE_TEST_DSN, future=True)

    test_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine_test, expire_on_commit=False
    )

    # Patch app.db.engine to be this SQLite engine.
    # This is important if any code directly uses app.db.engine.
    monkeypatch.setattr(db_module, "engine", engine_test)

    # Patch the session factory used by Depends(get_async_session)
    @asynccontextmanager
    async def _override_session() -> AsyncGenerator[AsyncSession, None]:
        async with test_session_maker() as session:
            yield session
    monkeypatch.setattr(db_module, "get_async_session", _override_session)

    # Also patch app.db.async_session (the sessionmaker) if it's used directly by any part of the app
    # (though get_async_session should be the primary way to get a session)
    monkeypatch.setattr(db_module, "async_session", test_session_maker)


    # Create tables.
    async def _init_models() -> None:
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all) # Drop all first for cleaner state
            await conn.run_sync(Base.metadata.create_all)

    asyncio.get_event_loop().run_until_complete(_init_models())

    app: FastAPI = create_app() # create_app should now use the patched settings/db
    return TestClient(app)
