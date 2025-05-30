import enum
from uuid import uuid4

from sqlalchemy import Column, String, Enum as SAEnum, ForeignKey, Date, DateTime, func, Text
from sqlalchemy.orm import relationship

# Consistent Base import with other models
from . import Base

class CommitteeRoleType(str, enum.Enum):
    leader = "leader"
    secretary = "secretary"
    treasurer = "treasurer"
    member = "member"
    coordinator = "coordinator"

class Committee(Base):
    __tablename__ = "committees"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    member_roles = relationship("CommitteeMemberRole", back_populates="committee", cascade="all, delete-orphan")
    # tasks = relationship("Task", back_populates="committee") # Add when Task model exists

class CommitteeMemberRole(Base):
    __tablename__ = "committee_member_roles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
    member_id = Column(String(36), ForeignKey("members.id"), nullable=False, index=True)
    committee_id = Column(String(36), ForeignKey("committees.id"), nullable=False, index=True)
    role = Column(SAEnum(CommitteeRoleType), nullable=False)
    
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    member = relationship("Member", back_populates="committee_assignments")
    committee = relationship("Committee", back_populates="member_roles")
