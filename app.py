import os
from flask import Flask, redirect, send_file, request, jsonify, abort
from models import Patient
from database import db
from models import DBSession

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


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


@app.route('/api/patient/<id>', methods=['GET'])
def read_patient(id):
    session = DBSession()
    patient = session.query(Patient).filter_by(id=id).one()
    session.close()
    return jsonify({
        "id": patient.id,
        "age": patient.age,
        "transport_type": patient.transport_type,
        "ward_area": patient.ward_area,
        "shift": patient.shift,
        "vascular_access": patient.vascular_access,
        "mobility": patient.mobility,
        "nurse_seniority": patient.nurse_seniority,
        "enter_waiting_room": patient.enter_waiting_room,
        "leave_waiting_room": patient.leave_waiting_room,
        "nurse_begins_prep": patient.nurse_begins_prep,
        "begin_dialysis": patient.begin_dialysis,
        "end_dialysis": patient.end_dialysis,
        "nurse_applies_bandage": patient.nurse_applies_bandage,
        "enter_waiting_room_done": patient.enter_waiting_room_done,
        "leave_waiting_room_done": patient.leave_waiting_room_done
    })


@app.route('/api/patient/<id>/data', methods=['POST'])
def update_patient(id):
    content = request.get_json(silent=True)
    session = DBSession()
    patient = session.query(Patient).filter_by(id=id).one()
    for key, value in content.iteritems():
        setattr(patient, key, value)
    stmt = session.add(patient)
    session.commit()
    session.close()
    return jsonify({})

#
# @app.route('/api/patient/create', methods=['POST'])
# def create_patient():
#     session = DBSession()
#     patient = Patient()
#     stmt = session.add(patient)
#     session.commit()
#     session.close()
#     return jsonify({})


def main():
    app.run("0.0.0.0")

if __name__ == '__main__':
    main()
