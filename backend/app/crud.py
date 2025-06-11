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


def get_unit(db: Session, unit_id: int):
    return db.get(models.Unit, unit_id)


def update_unit(db: Session, unit_id: int, unit: schemas.UnitCreate):
    obj = db.get(models.Unit, unit_id)
    if obj:
        obj.name = unit.name
        db.commit()
        db.refresh(obj)
    return obj


def delete_unit(db: Session, unit_id: int):
    obj = db.get(models.Unit, unit_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj


# Member CRUD


def create_member(db: Session, member: schemas.MemberCreate) -> models.Member:
    db_member = models.Member(
        name=member.name, email=member.email, unit_id=member.unit_id
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()


def get_member(db: Session, member_id: int):
    return db.get(models.Member, member_id)


def update_member(db: Session, member_id: int, member: schemas.MemberCreate):
    obj = db.get(models.Member, member_id)
    if obj:
        obj.name = member.name
        obj.email = member.email
        obj.unit_id = member.unit_id
        db.commit()
        db.refresh(obj)
    return obj


def delete_member(db: Session, member_id: int):
    obj = db.get(models.Member, member_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj


# Task CRUD


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(
        title=task.title,
        status=task.status or models.TaskStatus.todo,
        priority=task.priority or models.TaskPriority.medium,
        due_date=task.due_date,
        assignee_id=task.assignee_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int):
    return db.get(models.Task, task_id)


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    obj = db.get(models.Task, task_id)
    if obj:
        if task.title is not None:
            obj.title = task.title
        if task.status is not None:
            obj.status = models.TaskStatus(task.status)
        if task.priority is not None:
            obj.priority = models.TaskPriority(task.priority)
        if task.due_date is not None:
            obj.due_date = task.due_date
        if task.assignee_id is not None:
            obj.assignee_id = task.assignee_id
        db.commit()
        db.refresh(obj)
    return obj


def delete_task(db: Session, task_id: int):
    obj = db.get(models.Task, task_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
