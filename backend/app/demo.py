from sqlalchemy.orm import Session

from . import models
from .db import Base, engine, SessionLocal


def seed_demo_data(session: Session) -> None:
    """Insert demo Units, Members and Tasks if tables are empty."""
    if not session.query(models.Unit).first():
        session.add_all([
            models.Unit(name="101"),
            models.Unit(name="102"),
        ])
        session.commit()

    if not session.query(models.Member).first():
        session.add_all([
            models.Member(name="Alice", email="alice@example.com", unit_id=1),
            models.Member(name="Bob", email="bob@example.com", unit_id=2),
        ])
        session.commit()

    if not session.query(models.Task).first():
        session.add_all([
            models.Task(title="Paint hallway", assignee_id=1),
            models.Task(title="Fix sink", assignee_id=2),
        ])
        session.commit()


def reset_demo_db() -> None:
    """Drop all tables and recreate them with demo data."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        seed_demo_data(session)
