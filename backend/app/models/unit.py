"""Unit / Lot model stub.

Represents an apartment, townhouse, or lot owned/managed by the cooperative.
Contains minimal attributes for now; extended fields (floorplan, address,
share information) will be added later.
"""

from uuid import uuid4

from sqlalchemy import Column, String

from app.models import Base


class Unit(Base):
    __tablename__ = "units"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    label = Column(String, nullable=False)  # e.g., "Unit 2B" or "Lot #15"
