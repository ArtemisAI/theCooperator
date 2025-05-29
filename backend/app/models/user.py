"""User model stub.

Attributes (planned):
• id – UUID pk
• full_name, email, phone …
• hashed_password
• role – enum (resident, admin, observer)
• created_at / updated_at timestamps
"""

from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, String, func

from app.models import Base


class UserRole(str, Enum):  # type: ignore[call-arg]
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
    role = Column(Enum(UserRole), nullable=False, default=UserRole.resident)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
