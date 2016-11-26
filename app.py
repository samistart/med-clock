import os
from flask import Flask, jsonify, redirect, send_file
from models import Stage
from database import db
from models import DBSession

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


@app.route("/www/<fname>")
def www(fname):
    return send_file(os.path.join("www", fname))


@app.route('/')
def homepage():
    return redirect("/www/scan.html")


def main():
    app.run()


if __name__ == '__main__':
    main()
