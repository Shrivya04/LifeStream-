from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LifeStream Blood Management API",
    description="API for managing blood donors, inventory, and compatibility checks.",
    version="1.0.0"
)

@app.post("/people/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.create_person(db=db, person=person)

@app.get("/people/", response_model=List[schemas.Person])
def read_people(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_people(db, skip=skip, limit=limit)

@app.get("/people/{person_id}", response_model=schemas.Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@app.post("/bloodunits/", response_model=schemas.BloodUnit)
def create_blood_unit(unit: schemas.BloodUnitCreate, db: Session = Depends(get_db)):
    db_unit = crud.get_blood_unit_by_unique_id(db, unit_unique_id=unit.unit_id)
    if db_unit:
        raise HTTPException(status_code=400, detail="Blood Unit with this ID already exists")
    return crud.create_blood_unit(db=db, unit=unit)

@app.get("/bloodunits/", response_model=List[schemas.BloodUnit])
def read_blood_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_blood_units(db, skip=skip, limit=limit)

@app.get("/bloodunits/{unit_id}", response_model=schemas.BloodUnit)
def read_blood_unit(unit_id: int, db: Session = Depends(get_db)):
    db_unit = crud.get_blood_unit(db, unit_id=unit_id)
    if db_unit is None:
        raise HTTPException(status_code=404, detail="Blood unit not found")
    return db_unit

@app.post("/analyze/find_compatible_blood", response_model=List[schemas.BloodUnit])
def find_compatible_blood_units_api(request: schemas.BloodRequest, db: Session = Depends(get_db)):
    compatible_units = crud.find_compatible_blood_units(
        db,
        recipient_blood_group=request.recipient_blood_group,
        emergency_only=request.emergency_only
    )
    if not compatible_units:
        detail = "No compatible blood units found"
        if request.emergency_only:
            detail += ", including O- for emergency"
        raise HTTPException(status_code=404, detail=detail)
    return compatible_units

@app.get("/")
def read_root():
    return {"message": "LifeStream Blood Management API is running!"}
