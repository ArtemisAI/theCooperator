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

    # Configure structured logging
    # This should be one of the first things to do, to ensure all subsequent logs are structured.
    from app.core.logging import configure_logging
    configure_logging() # Assuming default log level is fine for startup.

    import structlog # Import structlog for application logging
    logger = structlog.get_logger(__name__)
    logger.info("FastAPI application configured and starting up...")

    # Initialize FastAPI app
    app = FastAPI(title="theCooperator API", version="0.1.0-DEV")

    # Register global error handlers
    from app.core.error_handlers import APIException, api_exception_handler, generic_exception_handler
    app.add_exception_handler(APIException, api_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # Enable CORS
    from fastapi.middleware.cors import CORSMiddleware
    from app.core.config import settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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
