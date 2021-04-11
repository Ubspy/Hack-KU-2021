from blockchain import *
from medicalChange import *
from cryptography.hazmat.primitives import serialization
from encoder import GeneralEncoder
from medicalHistory import *
import time

with open("key.pem", "rb") as privateKeyFile:
    privateKey = serialization.load_pem_private_key(
        privateKeyFile.read(),
        password=b"passphrase"
    )

patientChain = BlockChain(name="Jon Gibbon", dob="10/3/1984", ssn=734237689, privateKey=privateKey)

patientChain.newEdit(sign(MedicalChange('bloodType', 'B+'), privateKey))
patientChain.newEdit(sign(MedicalChange('email', 'jwgibbo@gmail.com'), privateKey))
patientChain.newEdit(sign(MedicalChange("phoneNumber", '7858640221'), privateKey))
patientChain.newBlock()

patientChain.newEdit(sign(MedicalChange("allergies", ['pollen', 'latex']), privateKey))
#patientChain.newEdit(sign(MedicalChange('healthConditions', ['asthma']), privateKey))
patientChain.newBlock()

patientChain.newEdit(sign(MedicalChange('allergies', ['bees']), privateKey))
patientChain.newEdit(sign(MedicalChange('measurements', ['180lbs', '185cm', '95.4 F', '100/70mmHg']), privateKey))
patientChain.newBlock()

finalHash = sha256(str(json.dumps(patientChain.chain, cls=GeneralEncoder)).encode('utf-8')).hexdigest()
print(f'Success! Final hash has a proof of {patientChain.lastBlock.proof}')

print("Here is what the block chain looks like with all the signed objects:")
#time.sleep(3)
print(json.dumps(patientChain, cls=GeneralEncoder))

print("Here is what the patient's medical record will look like in pure json:")
#time.sleep(3)

patientHistory = MedicalHistory(None, None, None)
for change in patientChain.items():
    print(change.change)
    patientHistory.addChange(change.change)

print(json.dumps(patientHistory, cls=GeneralEncoder))