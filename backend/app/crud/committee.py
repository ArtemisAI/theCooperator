from typing import List, Optional, Union, Dict, Any
from uuid import UUID # Retaining for type hint consistency, though model uses String

from sqlalchemy.orm import Session
# from sqlalchemy.sql.expression import delete # Not used in provided code, can be added if bulk delete is needed

# Assuming CRUDBase exists as per the subtask description.
# If not, this will need to be adapted or CRUDBase created.
from app.crud.base import CRUDBase
from app.models.committee import Committee, CommitteeMemberRole, CommitteeRoleType
from app.schemas.committee import (
    CommitteeCreate,
    CommitteeUpdate,
    CommitteeMemberRoleCreate,
    CommitteeMemberRoleUpdate
)

class CRUDCommittee(CRUDBase[Committee, CommitteeCreate, CommitteeUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Committee]:
        return db.query(Committee).filter(Committee.name == name).first()

    # Additional committee-specific CRUD methods can be added here

committee = CRUDCommittee(Committee)


class CRUDCommitteeMemberRole(CRUDBase[CommitteeMemberRole, CommitteeMemberRoleCreate, CommitteeMemberRoleUpdate]):
    def get_by_member_and_committee(
        self, db: Session, *, member_id: str, committee_id: str
    ) -> Optional[CommitteeMemberRole]:
        return (
            db.query(CommitteeMemberRole)
            .filter(CommitteeMemberRole.member_id == member_id, CommitteeMemberRole.committee_id == committee_id)
            .first()
        )

    def get_roles_for_member(self, db: Session, *, member_id: str) -> List[CommitteeMemberRole]:
        return db.query(CommitteeMemberRole).filter(CommitteeMemberRole.member_id == member_id).all()

    def get_members_in_committee(self, db: Session, *, committee_id: str) -> List[CommitteeMemberRole]:
        return db.query(CommitteeMemberRole).filter(CommitteeMemberRole.committee_id == committee_id).all()

    def update_role(
        self,
        db: Session,
        *,
        db_obj: CommitteeMemberRole, # Existing role object
        obj_in: Union[CommitteeMemberRoleUpdate, Dict[str, Any]]
    ) -> CommitteeMemberRole:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # update_data = obj_in.model_dump(exclude_unset=True) # Pydantic v2
            update_data = obj_in.dict(exclude_unset=True) # Pydantic v1
        
        # Ensure all fields in update_data are actual attributes of the CommitteeMemberRole model before passing to super
        # This is a simplified approach; a more robust way might involve checking model.__table__.columns
        # or relying on CRUDBase to handle it.
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def add_member_to_committee(
        self, db: Session, *, member_id: str, committee_id: str, role: CommitteeRoleType, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> CommitteeMemberRole: # Added 'date' import implicitly via schemas, but good to be aware
        # Check if already exists
        db_role = self.get_by_member_and_committee(db, member_id=member_id, committee_id=committee_id)
        if db_role:
            # Update role if different, or if dates are different
            needs_update = False
            if db_role.role != role:
                needs_update = True
            if start_date is not None and db_role.start_date != start_date:
                needs_update = True
            if end_date is not None and db_role.end_date != end_date: # check if end_date is provided
                needs_update = True
            
            if needs_update:
                 update_schema = CommitteeMemberRoleUpdate(role=role, start_date=start_date, end_date=end_date)
                 return self.update_role(db, db_obj=db_role, obj_in=update_schema)
            return db_role

        # Create new role assignment
        # Ensure IDs are strings as model uses String(36)
        role_in_create = CommitteeMemberRoleCreate(
            member_id=str(member_id), 
            committee_id=str(committee_id),
            role=role,
            start_date=start_date,
            end_date=end_date
        )
        return self.create(db, obj_in=role_in_create)

    def remove_member_from_committee(
        self, db: Session, *, member_id: str, committee_id: str
    ) -> Optional[CommitteeMemberRole]:
        db_obj = self.get_by_member_and_committee(db, member_id=member_id, committee_id=committee_id)
        if db_obj:
            # CRUDBase remove method typically takes the primary key 'id'
            return self.remove(db, id=db_obj.id) 
        return None # Or raise an error if not found

committee_member_role = CRUDCommitteeMemberRole(CommitteeMemberRole)
