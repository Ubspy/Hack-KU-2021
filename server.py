from flask import Flask, render_template, request, json
from medicalChange import * 
from cryptography.hazmat.primitives import serialization
import json
from datetime import datetime
from blockchain import *
import os

with open("public.pem", "rb") as publicKeyFile:
    publicKey = serialization.load_pem_public_key(
        publicKeyFile.read()
    )

with open("key.pem", "rb") as privateKeyFile:
    privateKey = serialization.load_pem_private_key(
        privateKeyFile.read(),
        password=b"passphrase"
    )

__name__ = "ChainedTogether"

app = Flask(__name__)
app.secret_key = b'G\x10\x01D\x1e\xbabV\x1bAD\x0e\xdd\xe8r$\xaf\xfef\x8f\n\xf6,\xbb'

@app.route('/')
def index():
    #return "Hello, Gay Ass!"
    return render_template('index.html')

@app.route('/authPatient')
def parientView():
    return render_template('index.html', data=getPatientJSON(None))

@app.route('/authDoctor')
def doctorView():
    return render_template('index.html', data=getPatientJSON(None))

@app.route('/requestPatientEdits', methods=['POST'])
def writePatientInfo():
    # Look how ass this is, request.form is a different dict type than normal, so we need to do to_dict
    # that's not enough though, that gives a dict with all the data in a key, so we need to turn that into a dict_keys
    # but then we just want the first one, so THEN we need to cast it to a list
    # then finally, we get the first element, fuck JS
    dataDict = json.loads(list(request.form.to_dict().keys())[0])

    # This turns the dictionary into a key value pair tuple
    changesFromPage = [(key, dataDict[key]) for key in dataDict]

    # This then creates signed medical change objects
    signedChanges = [sign(MedicalChange(change[0], change[1], datetime.now()), privateKey) for change in changesFromPage]

    # TODO: Get right block chain from the database
    patientChain = None # Will be a blockchain object

    # Stage all of these changes for the block, then create the block
    for change in signedChanges:
        patientChain.newEdit(change)

    patientChain.newBlock()

    return render_template('index.html')

def getPatientJSON(loginInfo):
    patientChain = None # Will be a blockchain object

    for chainFile in os.listdir('chains/'):
        file = open(chainFile, 'r')
        decodedChain = decodeBlockchain(file.read())
        file.close()

        patientChain = None

        nameField = next(change for change in decodedChain.chain[0]['medicalChanges'] if change['tag'] == 'name')
        dobField = next(change for change in decodedChain.chain[0]['medicalChanges'] if change['tag'] == 'dob')
        ssnField = next(change for change in decodedChain.chain[0]['medicalChanges'] if change['tag'] == 'ssn')

        if nameField['data'] == loginInfo['name'] and dobField['data'] == loginInfo['dob'] and ssnField['data'] == loginInfo['ssn']:
            patientChain = decodedChain

    return patientChain.getJSON()

if __name__ == "__main__":
    app.run()