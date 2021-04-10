from datetime import datetime
from dataclasses import dataclass
from medicalData import PatientMeasurements
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import json
from encoder import GeneralEncoder, Serializable

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
            timestamp=datetime.fromisoformat(dct['timestamp']),
        ),
        signature=bytes.fromhex(dct['signature'])
    )
    
class MedicalChangeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, MedicalSerializable):
            return o.getJSON()
        elif isinstance(o, datetime):
            return o.isoformat()
        else:
            return json.JSONEncoder.default(self, o)
    
def verify(signedchange: SignedMedicalChange, pubkey: rsa.RSAPublicKey):
    change = signedchange.change
    message = bytes(repr(change), 'utf-8')
    
    pubkey.verify(
        signedchange.signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
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
        return json.load(f, object_hook=medical_change_decoder)
    
