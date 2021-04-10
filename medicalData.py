from json import JSONEncoder
from dataclasses import dataclass
from typing import Optional

class MedicalDataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

@dataclass
class Date:
    month: int
    day: int
    year: int
    def getJSON(self, obj):
        return MedicalDataEncoder().encode(obj)

@dataclass
class PatientVisit:
    date: Date
    place: str
    doctor: str
    notes: str
    def getJSON(self, obj):
        return MedicalDataEncoder().encode(obj)

@dataclass
class Media:
    visit: PatientVisit
    media: None
    def getJSON(self, obj):
        return MedicalDataEncoder().encode(obj)

@dataclass
class PatientMeasurements:
    date: Date
    weight: Optional[float]
    height: Optional[float]
    bloodPressure: Optional[str]
    def getJSON(self, obj):
        return MedicalDataEncoder().encode(obj)

@dataclass
class HealthInsuranceInfo:
    name: str
    provider: str
    id: int
    group: str
    plan: str
    address:str
    def getJSON(self, obj):
        return MedicalDataEncoder().encode(obj)

@dataclass
class MedicalData:
    name: str
    email: str
    phoneNumber: int
    address: str
    dob: Date
    ssn: int
    measurements: list[PatientMeasurements]
    bloodType: str
    allergies: list[str]
    media: list[Media]
    healthConditions: list[str]
    recentVisits: list[PatientVisit]
    def getJSON(self, obj):
        return MedicalDataEncoder().encode(obj)