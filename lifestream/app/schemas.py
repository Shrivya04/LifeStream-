from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List
from .models import BloodGroupEnum

class PersonBase(BaseModel):
    name: str = Field(..., example="Jane Doe")
    contact_info: str = Field(..., example="+15551234")
    blood_group: BloodGroupEnum = Field(..., example="A+")

class BloodUnitBase(BaseModel):
    unit_id: str = Field(..., example="UBH987")
    blood_group: BloodGroupEnum = Field(..., example="A+")
    donation_date: date
    expiry_date: date
    status: str = Field("Available", example="Available")

class PersonCreate(PersonBase):
    pass

class BloodUnitCreate(BloodUnitBase):
    donor_id: Optional[int] = None

class Person(PersonBase):
    id: int
    donated_units: List["BloodUnit"] = []

    class Config:
        orm_mode = True

class BloodUnit(BloodUnitBase):
    id: int
    donor_id: Optional[int] = None
    donor: Optional[PersonBase] = None

    class Config:
        orm_mode = True

class BloodRequest(BaseModel):
    recipient_blood_group: BloodGroupEnum = Field(..., example="A+")
    emergency_only: bool = False

Person.update_forward_refs()