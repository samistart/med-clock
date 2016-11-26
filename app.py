import os
from flask import Flask, redirect, send_file, request, jsonify
from models import Stage, Patient, Experiment
from database import db
from models import DBSession

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


@app.route("/www/<path:fname>")
def www(fname):
    return send_file(os.path.join("www", fname))


@app.route('/')
def homepage():
    return redirect("/www/scan.html")

# fetches the patient data given an id
# returns the data associated with said patient
# as well as any stage timings that have been recorded


@app.route('/api/patient/<id>', methods=['GET', 'POST'])
def patient(id):
    content = request.get_json(silent=True)
    session = DBSession()
    result = session.query(Patient).filter_by(id=id).first()
    print content
    return jsonify({
        'age': result.age,
        'attributes': result.attributes
    })


@app.route('/api/experiment/<id>', methods=['GET', 'POST'])
def experiment(id):
    content = request.get_json(silent=True)
    session = DBSession()
    result = session.query(Experiment).filter_by(id=id).first()
    print content
    return jsonify({
        'name': result.name,
    })


@app.route('/api/patient/<experiment_id>', methods=['GET', 'POST'])
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
