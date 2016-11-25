import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TESTING = False
CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = "postgresql://samistart:my_password@localhost/sandpit"
SQLALCHEMY_TRACK_MODIFICATIONS = False