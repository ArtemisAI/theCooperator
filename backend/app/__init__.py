"""Top-level package for theCooperator backend.

This package follows the standard FastAPI project layout:

backend/app
├── __init__.py      (this file)
├── main.py          – application factory & entry-point
├── core/            – configuration, logging, security helpers
├── models/          – SQLAlchemy ORM models
├── schemas/         – Pydantic request/response models
├── services/        – business logic, domain services
├── api/             – versioned API routers (mounted in main.py)
└── jobs/            – Celery/APS background tasks

Only minimal scaffolding exists at this stage. Implementation will start in
Phase 0 of the roadmap.
"""

from importlib.metadata import version, PackageNotFoundError


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover – package not installed yet.
    __version__ = "0.0.0.dev"
