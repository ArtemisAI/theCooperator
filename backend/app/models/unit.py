import enum
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

# Assuming Base is defined in app.models or similar
# If Base is in app.database, change the import accordingly
from . import Base # Corrected: Base is now in app.models


class UnitStatus(str, enum.Enum):
    active = "active"
    vacant = "vacant"
    under_maintenance = "under_maintenance"


class Unit(Base):
    __tablename__ = "units"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    # label column will be replaced by unit_number as per new model
    unit_number = Column(String, unique=True, nullable=False, index=True)
    status = Column(Enum(UnitStatus), nullable=False, default=UnitStatus.active)
    # description can be added if it's in data_model_guidance.md, but it's not explicitly listed for Unit.
    # For now, I'm omitting it to strictly follow the new guidance for Unit.

    members = relationship("Member", back_populates="unit")

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
