from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import enum

class BloodGroupEnum(str, enum.Enum):
    APos = "A+"
    ANeg = "A-"
    BPos = "B+"
    BNeg = "B-"
    ABPos = "AB+"
    ABNeg = "AB-"
    OPos = "O+"
    ONeg = "O-"

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_info = Column(String)
    blood_group = Column(Enum(BloodGroupEnum), index=True)
    donated_units = relationship("BloodUnit", back_populates="donor")

class BloodUnit(Base):
    __tablename__ = "blood_inventory"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(String, unique=True, index=True)
    blood_group = Column(Enum(BloodGroupEnum), index=True)
    donation_date = Column(Date)
    expiry_date = Column(Date)
    status = Column(String, default="Available")
    donor_id = Column(Integer, ForeignKey("people.id"))
    donor = relationship("Person", back_populates="donated_units")
