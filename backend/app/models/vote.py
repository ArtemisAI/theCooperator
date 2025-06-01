"""Vote model stub.

Records an individual vote cast by a user on a proposal.
"""

from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.models import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    proposal_id = Column(String, ForeignKey("proposals.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    choice = Column(String, nullable=False) # e.g. "yes", "no", "abstain"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    proposal = relationship("Proposal", back_populates="votes")
    user = relationship("User", back_populates="votes")