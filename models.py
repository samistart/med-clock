import re
import datetime
from database import db
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Stage(Base):
    __tablename__ = 'Entry'
    experiment_id = Column('Experiment Id', Integer(), primary_key=True, nullable=False)
    patient_id = Column('Patient Id', Integer(), primary_key=True, nullable=False)
    stage = Column('Stage', Integer(), primary_key=True, nullable=False)
    start = Column('Timestamp', DateTime, default=datetime.datetime.now, index=True, nullable=False)
    end = Column('Timestamp', DateTime, default=datetime.datetime.now, index=True, nullable=False)

    def __init__(self, experiment_id, patient_id, stage, start, end):
        self.experiment_id = experiment_id
        self.patient_id = patient_id
        self.stage = stage
        self.start = start
        self.end = end

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)