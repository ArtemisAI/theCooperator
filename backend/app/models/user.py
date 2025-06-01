"""User model stub.

Attributes (planned):
• id – UUID pk
• full_name, email, phone …
• hashed_password
• role – enum (resident, admin, observer)
• created_at / updated_at timestamps
"""

from uuid import uuid4
import enum # Import Python's enum module

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Enum as SAEnum # Import SQLAlchemy's Enum explicitly

from app.models import Base


class UserRole(str, enum.Enum): # Inherit from enum.Enum
    resident = "resident"
    admin = "admin"
    observer = "observer"


class User(Base):
    """Minimal columns; will be expanded during Phase 1."""

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.resident) # Use SAEnum and pass the class
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    tasks = relationship("Task", back_populates="assignee")
    proposals = relationship("Proposal", back_populates="proposer")
    votes = relationship("Vote", back_populates="user")
    score_entries = relationship("ScoreEntry", back_populates="user")
