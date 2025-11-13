from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Set

def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def get_people(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_blood_unit(db: Session, unit_id: int):
    return db.query(models.BloodUnit).filter(models.BloodUnit.id == unit_id).first()

def get_blood_unit_by_unique_id(db: Session, unit_unique_id: str):
    return db.query(models.BloodUnit).filter(models.BloodUnit.unit_id == unit_unique_id).first()

def get_blood_units(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BloodUnit).offset(skip).limit(limit).all()

def create_blood_unit(db: Session, unit: schemas.BloodUnitCreate):
    db_unit = models.BloodUnit(**unit.dict())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

def get_compatible_donor_groups(recipient_blood_group: models.BloodGroupEnum) -> Set[models.BloodGroupEnum]:
    compatible_groups: Set[models.BloodGroupEnum] = set()
    abo_type = recipient_blood_group.value[0]
    rh_factor = recipient_blood_group.value[-1]

    if abo_type == 'A':
        compatible_groups.update({
            models.BloodGroupEnum.APos, models.BloodGroupEnum.ANeg,
            models.BloodGroupEnum.OPos, models.BloodGroupEnum.ONeg
        })
    elif abo_type == 'B':
        compatible_groups.update({
            models.BloodGroupEnum.BPos, models.BloodGroupEnum.BNeg,
            models.BloodGroupEnum.OPos, models.BloodGroupEnum.ONeg
        })
    elif abo_type == 'AB':
        compatible_groups.update({
            models.BloodGroupEnum.APos, models.BloodGroupEnum.ANeg,
            models.BloodGroupEnum.BPos, models.BloodGroupEnum.BNeg,
            models.BloodGroupEnum.ABPos, models.BloodGroupEnum.ABNeg,
            models.BloodGroupEnum.OPos, models.BloodGroupEnum.ONeg
        })
    elif abo_type == 'O':
        compatible_groups.update({
            models.BloodGroupEnum.OPos, models.BloodGroupEnum.ONeg
        })

    if rh_factor == '-':
        compatible_groups = {bg for bg in compatible_groups if bg.value[-1] == '-'}

    return compatible_groups

def find_compatible_blood_units(
    db: Session, 
    recipient_blood_group: models.BloodGroupEnum, 
    emergency_only: bool = False
) -> List[models.BloodUnit]:
    if emergency_only:
        compatible_units = db.query(models.BloodUnit).filter(
            models.BloodUnit.blood_group == models.BloodGroupEnum.ONeg,
            models.BloodUnit.status == "Available"
        ).all()
        if compatible_units:
            return compatible_units

    allowed_groups = get_compatible_donor_groups(recipient_blood_group)
    compatible_units = db.query(models.BloodUnit).filter(
        models.BloodUnit.blood_group.in_(list(allowed_groups)),
        models.BloodUnit.status == "Available"
    ).all()

    return compatible_units
