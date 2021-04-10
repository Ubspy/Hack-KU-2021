from time import time
from hashlib import sha256 
import medicalData
from json import JSONEncoder

# Encodes the block chain and the individual blocks 
class BlockChainEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, '__dict__'): # Check if there's a dict property, if so we return it, if not we use vars
            return vars(o)
        else:
            return o.__dict__

# Block chain class, handles adding new blocks
class BlockChain:
    def __init__(self):
        self.chain = [] # Block chain list
        self.pendingEdits = [] # Current edits to add to a new block
        self.chain.append(Block({}, 0, 0, 0)) # Adds an empty block at the beginning
        # TODO: Make this just add basic information for a new medical patient instead of an empty block

    # Gets the length of the block chain
    def chainLen(self):
        return len(self.chain)

    # Adds a new edit to the list of edits we will eventually add to a block
    def newEdit(self, medicalData):
        self.pendingEdits.append(medicalData)

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
        if self.validateChain(): # Check if the block chain is validated
            proof = self.proofOfWork(self.lastBlock) # Calculate the proof for this block
            block = Block(self.pendingEdits, len(self.chain), self.hashBlock(self.lastBlock), proof) # Create a new block object with the calculated proof
            self.chain.append(block) # Append this block
            self.pendingEdits = [] # Clear pending edits
        else:
            # TODO: Make this more explicit
            raise Exception("Failed to valitate blockchain! >:(")

    # Defines a property so we can get the last block in the chain
    @property
    def lastBlock(self):
        return self.chain[len(self.chain) - 1]

# Block class, takes a set of data, an index, a previous hash and a proof
class Block:
    def __init__(self, medicalData, index, previousHash, proof):
        self.time = time() # Keeps a time stamp for the block
        self.index = index
        self.medicalData = medicalData
        self.previousHash = previousHash
        self.proof = proof

    # Getters for medical data, index and JSON
    def getMedicalData(self):
        return self.medicalData

    def getIndex(self):
        return self.index

    def getJSON(self):
        return BlockChainEncoder().encode(self) # TODO: Sign blocks