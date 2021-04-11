from medicalChange import MedicalChange
import medicalData
from dataclasses import dataclass, field
import datetime
from encoder import Serializable
from typing import List, Set

@dataclass
class MedicalHistory(Serializable):
    name: str
    dob: datetime.date
    ssn: int
    emails: Set[str] = field(default_factory=set)
    phoneNumbers: Set[int] = field(default_factory=set)
    addresses: Set[str] = field(default_factory=set)
    measurements: List[medicalData.PatientMeasurements] = field(default_factory=list)
    bloodType: str = ""
    allergies: Set[medicalData.Allergy] = field(default_factory=set)
    # media: List[Media]
    healthConditions: List[str] = field(default_factory=list)
    # recentVisits: List[PatientVisit] = field(default_factory=list)
    
    def addChange(self, change: MedicalChange):
        def transaction(add_func, remove_func):
            def add_or_remove(transaction_tuple):
                if transaction_tuple[0] == "add":
                    add_func(transaction_tuple[1])
                elif transaction_tuple[0] == "remove":
                    remove_func(transaction_tuple[1])
            return add_or_remove
        if change.tag == "name":
            self.name = change.data
        elif change.tag == "email":
            transaction(self.emails.add, self.emails.discard)(change.data)
        elif change.tag == "phoneNumber":
            transaction(self.phoneNumbers.add, self.emails.discard)(change.data)
        elif change.tag == "address":
            transaction(self.addresses.add, self.addresses.discard)(change.data)
        elif change.tag == "dob":
            self.dob = change.data
        elif change.tag == "ssn":
            self.ssn = change.data
        elif change.tag == "measurements":
            self.measurements.append(change.data)
        elif change.tag == "bloodType":
            self.bloodType = change.data
        elif change.tag == "allergies":
            transaction(self.allergies.add, self.allergies.discard)(change.data)
        elif change.tag == "healthConditions":
            def remove_func(data):
                try:
                    self.healthConditions.remove(data)
                except ValueError:
                    pass
            transaction(self.healthConditions.add, remove_func)