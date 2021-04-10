from datetime import datetime
from dataclasses import dataclass
from medicalData import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
import json

@dataclass
class MedicalChange:
    tag: str
    data: any
    timestamp: datetime
    
@dataclass
class SignedMedicalChange:
    change: MedicalChange
    signature: bytes
    
    
def measurement_decoder(dct) -> PatientMeasurements:
    return PatientMeasurements(dct.get('weight'), dct.get('height'), dct.get('bloodPressure'))
    
data_decoders = {
    "measurement": measurement_decoder,
}

def medical_change_decoder(dct):
    return SignedMedicalChange(
        MedicalChange(
            tag=dct['type'], 
            data=data_decoders[dct['type']](dct['data']),
            timestamp=dct['timestamp'],
        ),
        signature=dct['signature']
    )
    
class MedicalChangeEncoder(json.JSONEncoder):
    def default(self, o: SignedMedicalChange):
        change = o.change
        return {
            "tag": change.tag,
            "data": change.data,
            "timestamp": change.timestamp,
            "signature": o.signature
        }
    
def verify(signedchange: SignedMedicalChange, pubkey: rsa.RSAPublicKey):
    change = signedchange.change
    message = bytes(repr(change))
    
    pubkey.verify(
        change.signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
def sign(change: MedicalChange, key: rsa.RSAPrivateKey) -> SignedMedicalChange:
    message = bytes(repr(change))
    signature = key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return SignedMedicalChange(change, signature)

def load(filename):
    with open(filename) as f:
        return json.load(f, object_hook=medical_change_decoder)
    
