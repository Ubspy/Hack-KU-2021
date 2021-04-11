from dataclasses import dataclass
from typing import Optional
from encoder import Serializable
import datetime

class MedicalData:
    pass
    
@dataclass
class PatientVisit(Serializable, MedicalData):
    date: datetime.date
    place: str
    doctor: str
    notes: str

@dataclass
class Media(Serializable, MedicalData):
    visit: PatientVisit
    media: None

@dataclass
class PatientMeasurements(Serializable, MedicalData):
    date: datetime.date
    weight: Optional[float]
    height: Optional[float]
    bloodPressure: Optional[str]
    
@dataclass
class Allergy(Serializable, MedicalData):
    allergen: str
    severity: str
    description: Optional[str] = ""
    def __hash__(self):
        return hash(self.allergen)
    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.allergen == other.allergen and
            self.severity == other.severity and
            self.description == other.description
        )

@dataclass
class HealthInsuranceInfo(Serializable, MedicalData):
    name: str
    provider: str
    id: int
    group: str
    plan: str
    address:str
