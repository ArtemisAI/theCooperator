from sqlalchemy.orm import Session

from . import models, schemas

# Unit CRUD

def create_unit(db: Session, unit: schemas.UnitCreate) -> models.Unit:
    db_unit = models.Unit(name=unit.name)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

def get_units(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Unit).offset(skip).limit(limit).all()

# Member CRUD

def create_member(db: Session, member: schemas.MemberCreate) -> models.Member:
    db_member = models.Member(name=member.name, email=member.email, unit_id=member.unit_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()

def get_member(db: Session, member_id: int):
    return db.get(models.Member, member_id)

def delete_member(db: Session, member_id: int):
    obj = db.get(models.Member, member_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
