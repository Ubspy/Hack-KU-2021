from flask import Flask, render_template
__name__ = "ChainedTogether"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authPatient')
def parientView():
    return None

@app.route('/authDoctor')
def doctorView():
    return None

@app.route('/requestPatientEdits', method=['POST'])
def writePatientInfo():
    