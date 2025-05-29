"""Proposal model stub.

Represents a proposal for voting within the cooperative.
"""

from uuid import uuid4
from sqlalchemy import Column, String, Text, DateTime, func
from app.models import Base


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())