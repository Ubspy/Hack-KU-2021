from dataclasses import dataclass
from typing import Optional, List
from encoder import Serializable
import datetime


@dataclass
class PatientVisit(Serializable):
    date: datetime.date
    place: str
    doctor: str
    notes: str

@dataclass
class Media(Serializable):
    visit: PatientVisit
    media: None

@dataclass
class PatientMeasurements(Serializable):
    date: datetime.date
    weight: Optional[float]
    height: Optional[float]
    bloodPressure: Optional[str]

@dataclass
class HealthInsuranceInfo(Serializable):
    name: str
    provider: str
    id: int
    group: str
    plan: str
    address:str

@dataclass
class MedicalData(Serializable):
    name: str
    email: str
    phoneNumber: int
    address: str
    dob: datetime.date
    ssn: int
    measurements: List[PatientMeasurements]
    bloodType: str
    allergies: List[str]
    media: List[Media]
    healthConditions: List[str]
    recentVisits: List[PatientVisit]
