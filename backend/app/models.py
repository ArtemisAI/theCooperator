from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .db import Base

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    members = relationship("Member", back_populates="unit")

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"))

    unit = relationship("Unit", back_populates="members")
