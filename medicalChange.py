from datetime import datetime
from dataclasses import dataclass
from medicalData import PatientMeasurements, MedicalData
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import json
from encoder import Serializable

@dataclass
class MedicalChange():
    tag: str
    data: MedicalData
    timestamp: datetime = datetime.now()
        
@dataclass
class SignedMedicalChange(Serializable):
    change: MedicalChange
    signature: bytes
    publicKey: bytes
    def getJSON(self):
        return {
            "tag": self.change.tag,
            "data": self.change.data,
            "timestamp": self.change.timestamp,
            "signature": self.signature.hex()
        }
        
@dataclass
class EncryptedMedicalChange(Serializable):
    encryptedChange: bytes
    patientSignature: bytes
    providerPublicKey: bytes
    providerSignature: bytes
    def getJSON(self):
        return {
            "encryptedChange": self.encryptedChange.hex(),
            "patientSignature": self.patientSignature.hex(),
            "providerPublicKey": self.providerPublicKey.hex(),
            "providerSignature": self.providerSignature.hex()
        }
    
def encryptForPatient(signedChange: SignedMedicalChange, patientPubKey: rsa.RSAPublicKey) -> EncryptedMedicalChange:
    message = bytes(repr(signedChange.change))
    return EncryptedMedicalChange(
        encryptedChange=patientPubKey.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ),
        patientSignature=None,
        providerPublicKey=signedChange.publicKey,
        providerSignature=signedChange.signature
    )
    
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
    
def verify(signedchange: SignedMedicalChange) -> bool:
    change = signedchange.change
    message = bytes(repr(change), 'utf-8')
    
    try:
        signedchange.publicKey.verify(
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
    
    
def sign(change: MedicalChange, privateKey: rsa.RSAPrivateKey) -> SignedMedicalChange:
    message = bytes(repr(change), 'utf-8')
    signature = privateKey.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    publicKey = privateKey.public_key()
    return SignedMedicalChange(change, signature, publicKey)
    

def load(filename):
    with open(filename) as f:
        return json.load(f, object_hook=medicalChangeDecoder)
    
