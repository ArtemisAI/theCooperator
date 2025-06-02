"""ScoreEntry model stub.

Represents a user's participation score entry at a point in time.
"""

from uuid import uuid4
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from app.models import Base


class ScoreEntry(Base):
    __tablename__ = "score_entries"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())