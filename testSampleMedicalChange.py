from medicalChange import *
from medicalData import *
from medicalHistory import MedicalHistory
from datetime import datetime, date
import json
from pprint import pprint
from cryptography.hazmat.primitives import serialization
from encoder import GeneralEncoder


myhistory = MedicalHistory(
    name="Andrew Riachi",
    dob=date(2000, 12, 5),
    ssn=8008135,
)

mychanges = [
    MedicalChange(
        "measurements",
        PatientMeasurements(
            date.today(), 
            170,
            None, 
            None
        ),
        datetime.now()
    ),

    MedicalChange(
        "measurements",
        PatientMeasurements(
            date.today(),
            171,
            None,
            None
        ),
        datetime.now()
    ),

    MedicalChange(
        "allergies",
        (
            "add",
            Allergy(
                allergen="ragweed",
                severity="mild"
            )
        ),
        datetime.now()
    ),

    MedicalChange(
        "allergies",
        (
            "add",
            Allergy(
                allergen="ragweed",
                severity="mild",
                description="this allergy sucks."
            )
        ),
        datetime.now()
    ),

    MedicalChange(
        "allergies",
        (
            "remove",
            Allergy(
                allergen="ragweed",
                severity="mild",
                description="this allergy sucks."
            )
        ),
        datetime.now()
    )
]

with open("key.pem", "rb") as private_key_file:
    private_key = serialization.load_pem_private_key(
        private_key_file.read(),
        password=b"passphrase"
    )

mysignedchanges = list(map(lambda change: sign(change, private_key), mychanges))

encoded = json.dumps(mysignedchanges, cls=GeneralEncoder)
print(encoded)

with open("public.pem", "rb") as public_key_file:
    public_key = serialization.load_pem_public_key(
        public_key_file.read()
    )

for signedchange in mysignedchanges:
    print(f"Change at {signedchange.change.timestamp} is verified!") if verify(signedchange, public_key) else print(f"Oops {signedchange.change.timestamp}")

for change in mychanges:
    myhistory.addChange(change)

print(myhistory)