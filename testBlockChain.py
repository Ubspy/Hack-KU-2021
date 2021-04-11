from blockchain import BlockChain, decodeBlockchain
from medicalHistory import MedicalHistory
from medicalChange import MedicalChange, sign, verify
from encoder import GeneralEncoder
from cryptography.hazmat.primitives import serialization
import json

with open("key.pem", "rb") as privateKeyFile:
    privateKey = serialization.load_pem_private_key(
        privateKeyFile.read(),
        password=b"passphrase"
    )


chain = BlockChain(name="Joe Biden", ssn=69420666, dob="4/15/1987", privateKey=privateKey)

chain.newEdit(sign(MedicalChange("bloodType", "A-"), privateKey))
chain.newBlock()

chain.newEdit(sign(MedicalChange("allergies", ['pollen', 'latex']), privateKey))
chain.newBlock()

chain.newEdit(sign(MedicalChange('bloodType', 'B+'), privateKey))
chain.newBlock()

chain.newEdit(sign(MedicalChange('allergies', ['pollen', 'latex', 'bees']), privateKey))
chain.newBlock()

chainstring = json.dumps(chain, cls=GeneralEncoder)
print(chainstring)

loadedchain = json.loads(chainstring, object_hook=decodeBlockchain)

print(json.dumps(loadedchain, cls=GeneralEncoder))