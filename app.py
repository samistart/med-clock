import os
from flask import Flask, jsonify, redirect, send_file
from flask_restful import Resource, Api
from models import Stage
from database import db
from models import DBSession

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
api = Api(app)


@app.route("/www/<fname>")
def www(fname):
    return send_file(os.path.join("www", fname))


@app.route('/')
def homepage():
    return redirect("/www/scan.html")

class Experiment(Resource):
    def get(self):
        return {'name': 'Dialysis'}


class Patient(Resource):
    def get(self):
        return {'name': 'Sami'}


api.add_resource(Experiment, '/experiment')
api.add_resource(Patient, '/patient')


@app.route('/experiment/<id>')
def get_experiment(id):
    print(id)
    return ""

# fetches the patient data given an id
# returns the data associated with said patient
# as well as any stage timings that have been recorded


@app.route('/patient/<id>')
def get_patient(id):
    print(id)
    return "output : data : {{name :    name, id   :   5, data_cols : [ 'age', 'height', 'anal_cavity'], stages : [ 'waiting', 'dialysis', 'weighing' ]}, stages : { dialysis : { start : '05:30', end : null }, waiting : { start : '04:30', end : '05:30' }, weighing : { start : null, end : null }}"

# # updates a patient record with data and a set of stage timings
# # returns nothing
#
# PUT
# /patient/<patientId>/stage/<stageId>/start
# input: timestamp
#
# PUT
# /patient/<patientId>/stage/<stageId>/end
# input : timestamp
#
# PUT
# /patient/<patientId>/data/
# input: dataObj

def main():
    app.run()


if __name__ == '__main__':
    main()
