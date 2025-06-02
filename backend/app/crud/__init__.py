"""CRUD helper modules.

Each sub-module contains the persistence logic for a given domain object. The
functions are intentionally **thin**; complex business rules belong in
`app.services.*` packages instead.
"""

from app.crud import user  # noqa: F401 – re-export for convenience.

__all__ = [
    "user",
    "unit",
]

