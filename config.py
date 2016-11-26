import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TESTING = False
CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = "postgresql://fivebitz:5bitzmisk@med-clock.cbmhjuzmjmi1.eu-west-1.rds.amazonaws.com:5432/sandpit"
SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "postgresql://samistart:xyhxMS69@localhost/sandpit"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True