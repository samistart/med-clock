from flask import Flask, render_template
from models import Stage
from database import db
from models import DBSession

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


@app.route('/')
def homepage():
    session = DBSession()
    stages = session.query(Stage)
    return render_template("stages.html", stages=stages)


if __name__ == '__main__':
    app.run()