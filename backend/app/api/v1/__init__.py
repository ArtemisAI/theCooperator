"""Version *v1* API router factory.

Additional endpoint sub-packages must be imported **inside** the function to
avoid circular imports when individual sub-modules also import this package.
"""

from __future__ import annotations

from fastapi import APIRouter


def get_api_router() -> APIRouter:  # noqa: D401 – factory.
    """Return router with all *v1* endpoints mounted."""

    router = APIRouter(prefix="/api/v1")

    # Import here to ensure models/config are ready.
    from app.api.v1.endpoints import auth, users, units, tasks, votes, metrics, todo  # noqa: WPS433 – runtime import

    router.include_router(auth.router)
    router.include_router(users.router)
    router.include_router(units.router)
    router.include_router(tasks.router)
    router.include_router(votes.router)
    router.include_router(metrics.router)
    router.include_router(todo.router, prefix="/todos", tags=["todos"])

    return router
