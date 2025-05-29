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

    # Build async SQLite engine.
    engine_test = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine_test, expire_on_commit=False
    )

    # Patch db.engine & dependency.
    db_module.engine = engine_test

    @asynccontextmanager
    async def _override_session() -> AsyncGenerator[AsyncSession, None]:  # noqa: WPS430
        async with session_maker() as session:  # noqa: WPS501
            yield session

    monkeypatch.setattr(db_module, "get_async_session", _override_session)

    # Create tables.
    async def _init_models() -> None:
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.get_event_loop().run_until_complete(_init_models())

    app: FastAPI = create_app()
    return TestClient(app)
