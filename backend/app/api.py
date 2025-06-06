from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .db import engine, Base
from .dependencies import get_db

Base.metadata.create_all(bind=engine)

# Seed demo data if database is empty
with engine.begin() as conn:
    if not conn.execute(models.Unit.__table__.select()).first():
        conn.execute(models.Unit.__table__.insert(), [{"name": "101"}, {"name": "102"}])
    if not conn.execute(models.Member.__table__.select()).first():
        conn.execute(
            models.Member.__table__.insert(),
            [
                {"name": "Alice", "email": "alice@example.com", "unit_id": 1},
                {"name": "Bob", "email": "bob@example.com", "unit_id": 2},
            ],
        )

app = FastAPI()

@app.post("/units/", response_model=schemas.Unit)
def create_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    return crud.create_unit(db, unit)

@app.get("/units/", response_model=list[schemas.Unit])
def read_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_units(db, skip=skip, limit=limit)

@app.post("/members/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    return crud.create_member(db, member)

@app.get("/members/", response_model=list[schemas.Member])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_members(db, skip=skip, limit=limit)

@app.get("/members/{member_id}", response_model=schemas.Member | None)
def read_member(member_id: int, db: Session = Depends(get_db)):
    return crud.get_member(db, member_id)

@app.delete("/members/{member_id}", response_model=schemas.Member | None)
def remove_member(member_id: int, db: Session = Depends(get_db)):
    return crud.delete_member(db, member_id)
