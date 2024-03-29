import os
from flask import Flask, redirect, send_file, request, jsonify, abort
from models import Patient
from database import db
from models import DBSession
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.route("/www/<path:fname>")
def www(fname):
    path = os.path.join( "www", fname )
    if not os.path.isfile(path):
        return abort( 404 )
    return send_file(path)


@app.route('/')
def homepage():
    return redirect("/www/scan.html")

# fetches the patient data given an id
# returns the data associated with said patient
# as well as any stage timings that have been recorded

def str_date( dt ):
    if dt is not None:
        dt = dt.isoformat()
    return dt

@app.route('/api/patient/<id>', methods=['GET'])
def read_patient(id):
    session = DBSession()
    patient = session.query(Patient).filter_by(id=id).one()
    session.close()
    return jsonify({
        "id": patient.id,
        "mac_address": patient.mac_address,
        "age": patient.age,
        "transport_type": patient.transport_type,
        "ward_area": patient.ward_area,
        "shift": patient.shift,
        "vascular_access": patient.vascular_access,
        "mobility": patient.mobility,
        "nurse_seniority": patient.nurse_seniority,
        "enter_waiting_room": str_date(patient.enter_waiting_room),
        "leave_waiting_room": str_date(patient.leave_waiting_room),
        "nurse_begins_prep": str_date(patient.nurse_begins_prep),
        "begin_dialysis": str_date(patient.begin_dialysis),
        "end_dialysis": str_date(patient.end_dialysis),
        "nurse_applies_bandage": str_date(patient.nurse_applies_bandage),
        "enter_waiting_room_done": str_date(patient.enter_waiting_room_done),
        "leave_waiting_room_done": str_date(patient.leave_waiting_room_done)
    })


@app.route("/api/macmap/<mac_address>", methods = ["GET"])
def get_patient_id(mac_address):
    content = request.get_json(silent=True)
    session = DBSession()
    patient = session.query(Patient).filter_by(mac_address=mac_address.upper()).first()
    id = patient.id if patient is not None else None
    session.close()
    return jsonify( id )


@app.route('/api/patient/<id>', methods=['PUT'])
def update_patient(id):
    content = request.get_json(silent=True)
    session = DBSession()
    patient = session.query(Patient).filter_by(id=id).one()
    for key, value in content.iteritems():
        setattr(patient, key, value)
    stmt = session.add(patient)
    session.commit()
    session.close()
    return jsonify()


@app.route('/api/patient', methods=['POST'])
def create_patient():
    content = request.get_json(silent=True)
    session = DBSession()
    session.expire_on_commit = False
    patient = Patient()
    if content and ("mac_address" in content):
        patient.mac_address = content["mac_address"].upper()
    stmt = session.add(patient)
    print(patient.id)
    session.commit()
    id = patient.id
    print(patient.id)
    session.close()
    return jsonify(patient.id)


def main():
    app.run("0.0.0.0")

if __name__ == '__main__':
    main()
