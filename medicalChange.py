from datetime import datetime
from dataclasses import dataclass
from medicalData import PatientMeasurements
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import json
from encoder import Serializable

@dataclass
class MedicalChange():
    tag: str
    data: any
    timestamp: datetime
        
@dataclass
class SignedMedicalChange(Serializable):
    change: MedicalChange
    signature: bytes
    def getJSON(self):
        return {
            "tag": self.change.tag,
            "data": self.change.data,
            "timestamp": self.change.timestamp,
            "signature": self.signature.hex()
        }
    
    
def measurementDecoder(dct) -> PatientMeasurements:
    return PatientMeasurements(dct.get('weight'), dct.get('height'), dct.get('bloodPressure'))
    
data_decoders = {
    "measurement": measurementDecoder,
}

def medicalChangeDecoder(dct):
    return SignedMedicalChange(
        MedicalChange(
            tag=dct['type'], 
            data=data_decoders[dct['type']](dct['data']),
            timestamp=datetime.fromisoformat(dct['timestamp']),
        ),
        signature=bytes.fromhex(dct['signature'])
    )
    
def verify(signedchange: SignedMedicalChange, pubkey: rsa.RSAPublicKey) -> bool:
    change = signedchange.change
    message = bytes(repr(change), 'utf-8')
    
    try:
        pubkey.verify(
            signedchange.signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except InvalidSignature:
        return False
    return True
    
    
def sign(change: MedicalChange, key: rsa.RSAPrivateKey) -> SignedMedicalChange:
    message = bytes(repr(change), 'utf-8')
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
        return json.load(f, object_hook=medicalChangeDecoder)
    
