from flask import Flask, render_template, request, json, redirect, url_for
from medicalChange import * 
from cryptography.hazmat.primitives import serialization
import json
from datetime import datetime
from blockchain import *
import os
from encoder import GeneralEncoder
from medicalHistory import MedicalHistory

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

# Load block chain dumps into a list
patientChains = []

for chainFile in os.listdir('chains/'):
    file = open(f'chains/{chainFile}', 'r')
    patientChains.append(decodeBlockchain(json.loads(file.read())))
    file.close()

@app.route('/')
def index():
    #return "Hello, Gay Ass!"
    return render_template('index.html')

@app.route('/viewPatient', methods=['GET', 'POST'])
def patientView():
    # if request.method == 'POST':
    #     dataDict = json.loads(list(request.form.to_dict().keys())[0])
    #     patientChain = getPatientChain(dataDict['creationInfo'])
    #     print(getPatientJson(patientChain))
    # else:
    return render_template('patient.html')

@app.route('/editPatient', methods=['GET'])
def doctorView():
    print(request.args)
    return render_template('index.html', data=data)

@app.route('/newPatient', methods=['POST'])
def newPatient():
    dataDict = json.loads(list(request.form.to_dict().keys())[0])
    print(dataDict)
    newPatientData = dataDict["creationInfo"]

    newPatient = BlockChain(name=newPatientData['name'], dob=newPatientData['dob'], ssn=newPatientData['ssn'], privateKey=privateKey)
    patientChains.append(newPatient)

    print(newPatient)

    newPatientFileName = newPatient.hashBlock(newPatient.chain[0]) + '.bloq'
    # newPatientFile = open(f'chains/{newPatientFileName}', 'w+')
    # newPatientFile.write(json.dumps(newPatient, cls=GeneralEncoder))
    # newPatientFile.close()

    # TODO: Make this render patient edit page
    #return render_template('index.html', data=getPatientJson(newPatient))
    return redirect(url_for('patientView'))

@app.route('/requestPatientEdits', methods=['POST'])
def writePatientInfo():
    # Look how ass this is, request.form is a different dict type than normal, so we need to do to_dict
    # that's not enough though, that gives a dict with all the data in a key, so we need to turn that into a dict_keys
    # but then we just want the first one, so THEN we need to cast it to a list
    # then finally, we get the first element, fuck JS
    dataDict = json.loads(list(request.form.to_dict().keys())[0])    

    # This turns the dictionary into a key value pair tuple
    changesFromPage = [(key, dataDict["block"][key]) for key in dataDict["block"]]

    # This then creates signed medical change objects
    signedChanges = [sign(MedicalChange(change[0], change[1], datetime.now()), privateKey) for change in changesFromPage]

    # TODO: Fix this
    patientChain = getPatientChain(dataDict["creationInfo"])
    #print(patientChain.getJSON())

    if patientChain:
        # Stage all of these changes for the block, then create the block
        for change in signedChanges:
            patientChain.newEdit(change)

        print(json.dumps(patientChain, cls=GeneralEncoder))
        print("Getting proof of work...")
        patientChain.newBlock()
        print("Got proof of work!")

        #fileName = patientChain.hashBlock(patientChain.chain[0]) + ".bloq"
        #outFile = open(f'chains/{fileName}', 'w')
        #outFile.write(patientChain.getJSON())

    # TODO: error?
    return render_template('index.html')

def getPatientChain(creationInfo):
    queriedChain = None # Will be a blockchain object

    for chain in patientChains:
        nameField = next(change for change in chain.chain[0].medicalChanges if change['tag'] == 'name')
        dobField = next(change for change in chain.chain[0].medicalChanges if change['tag'] == 'dob')
        ssnField = next(change for change in chain.chain[0].medicalChanges if change['tag'] == 'ssn')

        if nameField['data'] == creationInfo['name'] and dobField['data'] == creationInfo['dob'] and int(ssnField['data']) == int(creationInfo['ssn']):
            queriedChain = chain

    return queriedChain

def getPatientJson(patientChain):
    patientHistory = MedicalHistory(None, None, None)

    for change in patientChain.items():
        if change.change:
            patientHistory.addChange(change.change)
        else:
            patientHistory.addChange(decodeChange(change))

    return json.dumps(patientHistory, cls=GeneralEncoder)

if __name__ == "__main__":
    app.run()