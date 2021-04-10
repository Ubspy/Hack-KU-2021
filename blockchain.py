from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pendingEdits = []

    def newEdit(self, medicalData):
        self.pendingEdits.append(medicalData)

    def newBlock(self,proof, previousHash=None):
        block = Block(self.pendingEdits, self.lastBlock, hash(self.lastBlock))
        self.chain.append(block)

    @property
    def lastBlock(self):
        return self.chain[len(self.chain) - 1]

class Block:
    def __init__(self, medicalData, index, previousHash):
        self.time = time()
        self.index = index
        self.medicalData = medicalData
        self.hash = hash(medicalData)
        self.previousHash = previousHash

    def getMedicalData(self):
        return self.medicalData

    def getIndex(self):
        return self.index

    def getHash(self):
        return self.hash

class MedicalData:
    def __init__(self, name, dob, conditions):
        self.name = name
        self.dob = dob
