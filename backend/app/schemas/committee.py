from __future__ import annotations  # Important for forward references in type hints

from typing import List, Optional
from uuid import UUID # For type hinting, actual model uses str for id
from datetime import date, datetime # For type hinting created_at/updated_at if needed in schemas

from pydantic import BaseModel, Field, EmailStr # Added EmailStr
from app.models.committee import CommitteeRoleType # Import the enum

# Forward reference for MemberRead in CommitteeMemberRoleRead
class MemberReadMinimal(BaseModel): # A minimal representation of a Member
    id: str # Assuming UUIDs are stored as strings in the model
    email: EmailStr # Using Pydantic's EmailStr
    first_name: str
    last_name: str

    class Config:
        # from_attributes = True # Pydantic v2
        orm_mode = True # Pydantic v1
        use_enum_values = True


# Schema for CommitteeMemberRole
class CommitteeMemberRoleBase(BaseModel):
    member_id: str = Field(..., examples=["uuid-of-member"]) # Model uses String(36)
    committee_id: str = Field(..., examples=["uuid-of-committee"]) # Model uses String(36)
    role: CommitteeRoleType = Field(..., examples=[CommitteeRoleType.member])
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    class Config:
        use_enum_values = True

class CommitteeMemberRoleCreate(CommitteeMemberRoleBase):
    pass

class CommitteeMemberRoleUpdate(BaseModel):
    role: Optional[CommitteeRoleType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    class Config:
        use_enum_values = True

class CommitteeMemberRoleRead(CommitteeMemberRoleBase):
    id: str # Model uses String(36)
    member: MemberReadMinimal # Nested member information
    # committee: CommitteeReadMinimal (if needed, define CommitteeReadMinimal to avoid circularity)
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        # from_attributes = True
        orm_mode = True
        use_enum_values = True


# Schema for Committee
class CommitteeBase(BaseModel):
    name: str = Field(..., examples=["Finance Committee"])
    description: Optional[str] = Field(None, examples=["Manages the cooperative's finances."])

class CommitteeCreate(CommitteeBase):
    pass

class CommitteeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CommitteeRead(CommitteeBase):
    id: str # Model uses String(36)
    member_roles: List[CommitteeMemberRoleRead] = [] # List of members with their roles
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        # from_attributes = True
        orm_mode = True
        use_enum_values = True

# Minimal version for CommitteeMemberRoleRead to avoid circularity if CommitteeRead is nested there
# class CommitteeReadMinimal(CommitteeBase):
# id: str
# class Config:
# from_attributes = True
# # orm_mode = True
