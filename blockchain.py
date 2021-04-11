from time import time
from hashlib import sha256 
import medicalChange
from encoder import Serializable
from medicalChange import *
from cryptography.hazmat.primitives import serialization

with open("public.pem", "rb") as publicKeyFile:
    publicKey = serialization.load_pem_public_key(
        publicKeyFile.read()
    )

with open("key.pem", "rb") as privateKeyFile:
    privateKey = serialization.load_pem_private_key(
        privateKeyFile.read(),
        password=b"passphrase"
    )

# Block chain class, handles adding new blocks
class BlockChain(Serializable):
    def __init__(self, name, dob, ssn):
        self.chain = [] # Block chain list
        self.pendingEdits = [] # Current edits to add to a new block

        firstChange = []
        firstChange.append(sign(MedicalChange('name', name, datetime.timestamp), privateKey, publicKey))
        firstChange.append(sign(MedicalChange('dob', dob, datetime.timestamp), privateKey, publicKey))
        firstChange.append(sign(MedicalChange('ssn', ssn, datetime.timestamp), privateKey, publicKey))

        self.chain.append(Block(firstChange, 0, ssn, 0)) # Adds an empty block at the beginning
        # TODO: Make this just add basic information for a new medical patient instead of an empty block

    # Gets the length of the block chain
    def chainLen(self):
        return len(self.chain)

    # Adds a new edit to the list of edits we will eventually add to a block
    def newEdit(self, medicalChange):
        self.pendingEdits.append(medicalChange)

    # Gets the SHA256 hash for a block, turns the block data into JSON, then encodes it to utf-8, and then gets the SHA hash as a string
    def hashBlock(self, block):
        return sha256(str(block.getJSON()).encode('utf-8')).hexdigest()

    # Validates the whole chain by checking the previous hash stored in each block with the calculated hash from the block itself
    def validateChain(self, index=0):
        if index == len(self.chain):
            return True # Base case of recursion, returns True if we reach the end
        elif index > 0:
            # Recursive case, check stored previous hash with the calculated has, as well as the validation for the next part of the chain
            return (self.chain[index].previousHash == self.hashBlock(self.chain[index - 1])) and self.validateChain(index + 1)
        else:
            return self.validateChain(index + 1) # Can't compare the first element to the previous one, so we just return the next index
        
    # Validates all the signatures on the changes for patient medical data
    def validateSignatures(self, index=0):
        if index == len(self.chain):
            return True
        elif index > 0:
            return verify(self.chain[index].medicalChange) and self.validateSignatures(index+1)
        else:
            return self.validateChain(index + 1)

    # Checks is a proof is validated
    def isValidProof(self, lastProof, previousHash, proof):
        currentHash = sha256(str(f'{lastProof}{previousHash}{proof}').encode('utf-8'))
        return currentHash.hexdigest()[:5] == '00000' # TODO: Make this larger, I'm keeping smaller for implementation purposes

    # Function to calculate proof of work
    def proofOfWork(self, lastBlock):
        proof = 0 # Start with proof at 0, and check if it's a valid proof
        while not self.isValidProof(lastBlock.proof, self.hashBlock(lastBlock), proof):
            proof += 1 # If it's not valid, we add 1 and check again
        return proof

    # Create a new block, we have a previousHash variable for the first block
    def newBlock(self, previousHash=None):
        # Check if the block chain is validated and if the signatures are validated
        if self.validateChain() and self.validateSignatures():
            proof = self.proofOfWork(self.lastBlock) # Calculate the proof for this block
            block = Block(self.pendingEdits, len(self.chain), self.hashBlock(self.lastBlock), proof) # Create a new block object with the calculated proof
            self.chain.append(block) # Append this block
            self.pendingEdits = [] # Clear pending edits
        else:
            # TODO: Make this more explicit
            raise Exception("Failed to valitate blockchain! >:(")
    
    def getPatientInfoFromChain(self):
        patientInfo = {} # Empty dictionary

        for changes in [block.medicalChange for block in self.chain]:
            if changes:
                patientInfo.update(dict((change.change.tag, change.change.data) for change in changes))

        return patientInfo

    # Defines a property so we can get the last block in the chain
    @property
    def lastBlock(self):
        return self.chain[len(self.chain) - 1]

# Block class, takes a set of data, an index, a previous hash and a proof
class Block(Serializable):
    def __init__(self, medicalChange, index, previousHash, proof):
        self.time = time() # Keeps a time stamp for the block
        self.index = index
        self.medicalChange = medicalChange
        self.previousHash = previousHash
        self.proof = proof

    # Getters for medical data, index and JSON
    def getMedicalData(self):
        return self.medicalChange

    def getIndex(self):
        return self.index



chain = BlockChain("Joe Biden", "4/15/1987", 66642069)

chain.newEdit(sign(MedicalChange("bloodType", "A-", None), privateKey, publicKey))
chain.newBlock()

chain.newEdit(sign(MedicalChange("allergies", ['pollen', 'latex'], None), privateKey, publicKey))
chain.newBlock()

chain.newEdit(sign(MedicalChange('bloodType', 'B+', None), privateKey, publicKey))
chain.newBlock()

chain.newEdit(sign(MedicalChange('allergies', ['pollen', 'latex', 'bees'], None), privateKey, publicKey))
chain.newBlock()    

dictThing = chain.getPatientInfoFromChain()
print(dictThing)