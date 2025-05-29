# FastAPI application entry-point for theCooperator backend.

from fastapi import FastAPI
# SQLAlchemy metadata import so that table models are registered before
# `create_all()` is invoked during app start-up.

from app.models import Base  # noqa: F401 – imported for side-effects

from app.api.v1 import get_api_router
from app.db import engine


def create_app() -> FastAPI:
    """Factory function that instantiates and returns a FastAPI app.

    During Phase 0 we only register a bare bones health-check endpoint. Later
    phases will mount versioned API routers and add middleware (auth, CORS, …).
    """

    app = FastAPI(title="theCooperator API", version="0.1.0-DEV")

    # Mount API routers ------------------------------------------------------
    app.include_router(get_api_router())

    # Ensure tables exist in dev environment --------------------------------

    @app.on_event("startup")
    async def _create_tables() -> None:  # noqa: WPS430 – internal function.
        """Create missing tables (non-migrated dev env only).

        In production we will rely on *Alembic* migrations instead and remove
        this helper.
        """

        async with engine.begin() as conn:  # noqa: WPS501 – context manager OK
            await conn.run_sync(Base.metadata.create_all)

    @app.get("/health", tags=["meta"])
    async def healthcheck() -> dict[str, str]:
        """Lightweight liveness probe used by Docker/K8s."""

        return {"status": "ok"}

    return app


# Uvicorn entry-point when `python -m backend.app.main` is executed.
app = create_app()
