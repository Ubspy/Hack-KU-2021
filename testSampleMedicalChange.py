from medicalChange import *
from medicalData import *
from datetime import datetime
import json
from pprint import pprint
from cryptography.hazmat.primitives import serialization
from encoder import GeneralEncoder

mychange = MedicalChange(
    "measurements", 
    PatientMeasurements(
        Date(4, 10, 2021), 
        170,
        None, 
        None
    ),
    datetime.now()
)

with open("key.pem", "rb") as private_key_file:
    private_key = serialization.load_pem_private_key(
        private_key_file.read(),
        password=b"passphrase"
    )
signedchange = sign(mychange, private_key)

signedchange.change.data.weight = 170

encoded = json.dumps(signedchange, cls=GeneralEncoder)
print(encoded)

with open("public.pem", "rb") as public_key_file:
    public_key = serialization.load_pem_public_key(
        public_key_file.read()
    )

verify(signedchange, public_key)