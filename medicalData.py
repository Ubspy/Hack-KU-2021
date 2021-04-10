from json import JSONEncoder
from dataclasses import dataclass
from typing import Optional, List

class MedicalSerializable():
    def getJSON(self):
        return self.__dict__

@dataclass
class Date(MedicalSerializable):
    month: int
    day: int
    year: int
    def getJSON(self):
        return f"{self.year}-{self.month}-{self.day}"

@dataclass
class PatientVisit(MedicalSerializable):
    date: Date
    place: str
    doctor: str
    notes: str

@dataclass
class Media(MedicalSerializable):
    visit: PatientVisit
    media: None

@dataclass
class PatientMeasurements(MedicalSerializable):
    date: Date
    weight: Optional[float]
    height: Optional[float]
    bloodPressure: Optional[str]

@dataclass
class HealthInsuranceInfo(MedicalSerializable):
    name: str
    provider: str
    id: int
    group: str
    plan: str
    address:str

@dataclass
class MedicalData(MedicalSerializable):
    name: str
    email: str
    phoneNumber: int
    address: str
    dob: Date
    ssn: int
    measurements: List[PatientMeasurements]
    bloodType: str
    allergies: List[str]
    media: List[Media]
    healthConditions: List[str]
    recentVisits: List[PatientVisit]
