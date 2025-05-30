"""Member model.

Represents an individual residing in a unit and/or participating in the cooperative's activities.
"""

import enum
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum as SAEnum, String, func, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship

# Assuming Base is defined in app.models or similar
# If Base is in app.database, change the import accordingly
from . import Base # Corrected: Base is now in app.models
from .committee import CommitteeMemberRole


class MemberSex(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"


class MemberType(str, enum.Enum):
    primary = "primary"
    secondary = "secondary"


class Member(Base):
    __tablename__ = "members"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
    sex = Column(SAEnum(MemberSex), nullable=True)
    skills = Column(JSON, nullable=True)
    education_level = Column(String, nullable=True)
    member_type = Column(SAEnum(MemberType), nullable=False)
    legacy_full_name = Column(String, nullable=True) # Renamed from full_name

    unit_id = Column(String, ForeignKey("units.id"), nullable=True)
    unit = relationship("Unit", back_populates="members")

    committee_assignments = relationship(CommitteeMemberRole, back_populates="member")
    # Relationships to Task (defined as strings for now, will be updated when Task model is created)
    created_tasks = relationship("Task", foreign_keys="[Task.created_by_member_id]", back_populates="creator")
    assigned_tasks = relationship("Task", foreign_keys="[Task.assigned_to_member_id]", back_populates="assignee")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
