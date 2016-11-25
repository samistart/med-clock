import re
import datetime
from database import db
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Experiment(Base):
    __tablename__ = 'Experiment'
    id = Column('Id', Integer(), primary_key=True, nullable=False)
    name = Column('Name', String(), nullable=False)

    def __init__(self, name):
        self.name = name


class Patient(Base):
    __tablename__ = 'Patient'
    id = Column('Id', Integer(), primary_key=True, nullable=False)
    age = Column('Age', Integer(), nullable=False)
    attributes = Column('Age', String(), nullable=True)

    def __init__(self, age, attributes):
        self.age = age
        self.attributes = attributes


class Stage(Base):
    __tablename__ = 'Stage'
    experiment_id = Column('Experiment Id', Integer(), primary_key=True, nullable=False)
    patient_id = Column('Patient Id', Integer(), primary_key=True, nullable=False)
    number = Column('Number', Integer(), primary_key=True, nullable=False)
    name = Column('Name', String(), nullable=False)
    start = Column('Timestamp', DateTime, default=datetime.datetime.now, index=True, nullable=False)
    end = Column('Timestamp', DateTime, default=datetime.datetime.now, index=True, nullable=False)

    def __init__(self, experiment_id, patient_id, number, name, start, end):
        self.experiment_id = experiment_id
        self.patient_id = patient_id
        self.number = number
        self.name = name
        self.start = start
        self.end = end

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)