import os
from flask import Flask, redirect, send_file, request, jsonify
from models import Patient
from database import db
from models import DBSession

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


@app.route("/www/<dir>/<fname>")
def www(dir, fname):
    return send_file(os.path.join("www", dir, fname))


@app.route('/')
def homepage():
    return redirect("/www/scan.html")

# fetches the patient data given an id
# returns the data associated with said patient
# as well as any stage timings that have been recorded


@app.route('/api/patient/<id>', methods=['GET'])
def read_patient(id):
    session = DBSession()
    result = session.query(Patient).filter_by(id=id).one()
    return jsonify({
        "id": result.id,
        "age": result.age,
        "male": result.male,
        "transport_type": result.transport_type,
        "ward_area": result.ward_area,
        "shift": result.shift,
        "vascular_access": result.vascular_access,
        "mobility": result.mobility,
        "nurse_seniority": result.nurse_seniority,
        "enter_waiting_room": result.enter_waiting_room,
        "leave_waiting_room": result.leave_waiting_room,
        "nurse_begins_prep": result.nurse_begins_prep,
        "begin_dialysis": result.begin_dialysis,
        "end_dialysis": result.end_dialysis,
        "nurse_applies_bandage": result.nurse_applies_bandage,
        "enter_waiting_room_done": result.enter_waiting_room_done,
        "leave_waiting_room_done": result.leave_waiting_room_done
    })


@app.route('/api/patient/<id>/data', methods=['POST'])
def update_patient(id):
    content = request.get_json(silent=True)
    session = DBSession()
    result = session.query(Patient).filter_by(id=id).first()
    print content
    return jsonify({
        "id": result.id,
        "age": result.age,
        "male": result.male,
        "transport_type": result.transport_type,
        "ward_area": result.ward_area,
        "shift": result.shift,
        "vascular_access": result.vascular_access,
        "mobility": result.mobility,
        "nurse_seniority": result.nurse_seniority,
        "enter_waiting_room": result.enter_waiting_room,
        "leave_waiting_room": result.leave_waiting_room,
        "nurse_begins_prep": result.nurse_begins_prep,
        "begin_dialysis": result.begin_dialysis,
        "end_dialysis": result.end_dialysis,
        "nurse_applies_bandage": result.nurse_applies_bandage,
        "enter_waiting_room_done": result.enter_waiting_room_done,
        "leave_waiting_room_done": result.leave_waiting_room_done
    })


@app.route('/api/patient/<id>/events', methods=['GET', 'POST'])
def stage(experiment_id):
    content = request.get_json(silent=False)
    print(content)
    session = DBSession()
    results = session.query(Stage).filter_by(experiment_id=experiment_id)
    results_json = {}
    for i, result in enumerate(results):
        results_json[i] = {
            'name': result.name,
        }
    return jsonify(results_json)


def main():
    app.run()

if __name__ == '__main__':
    main()