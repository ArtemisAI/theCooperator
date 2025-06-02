"""SQLAlchemy ORM models – placeholder stage.

In later phases we will implement actual tables and relationships. For now we
only declare a `Base` instance so alembic can establish a migration baseline.
"""

from sqlalchemy.orm import declarative_base


Base = declarative_base()

# Import model classes so that they are registered on *Base.metadata*.
# This is required for `create_all()` and alembic autogeneration to discover
# tables. Keep these imports at the bottom to avoid circular dependencies.

from app.models import user, unit, task, proposal, vote, score_entry  # noqa: WPS433,F401 – import for side-effects.
