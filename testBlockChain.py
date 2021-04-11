from blockchain import BlockChain, decode_blockchain
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


chain = BlockChain()

chain.newEdit(sign(MedicalChange("name", "Joe Biden"), privateKey))
chain.newEdit(sign(MedicalChange("bloodType", "A-"), privateKey))
chain.newEdit(sign(MedicalChange("dob", "4/15/1987"), privateKey))
chain.newBlock()

chain.newEdit(sign(MedicalChange("allergies", ['pollen', 'latex']), privateKey))
chain.newBlock()

chain.newEdit(sign(MedicalChange('bloodType', 'B+'), privateKey))
chain.newBlock()

chain.newEdit(sign(MedicalChange('allergies', ['pollen', 'latex', 'bees']), privateKey))
chain.newBlock()

history = MedicalHistory("Joe Biden", "4/15/1987", 385762048)

for signedchange in chain.items():
    if verify(signedchange):
        print(f"Verified change at {signedchange.change.timestamp}!")
        history.addChange(signedchange.change)
    else:
        print(f"ERROR: Change at {signedchange.change.timestamp} was not authorized by a healthcare provider! Not adding.")

print(json.dumps(history, cls=GeneralEncoder))

chainstring = json.dumps(chain, cls=GeneralEncoder)
print(chainstring)

loadedchain = json.loads(chainstring, object_hook=decode_blockchain)

print(json.dumps(loadedchain, cls=GeneralEncoder))