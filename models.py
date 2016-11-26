import re
import datetime
from database import db
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Patient(Base):
    __tablename__ = 'Patient'
    id = Column('Id', Integer(), primary_key=True, nullable=False, autoincrement=True)
    mac_address = Column('mac_address', String(), unique=True)
    age = Column('Age', Integer())
    transport_type = Column('transport_type', String())
    ward_area = Column('ward_area', String())
    shift = Column('shift', String())
    vascular_access = Column('vascular_access', String())
    mobility = Column('mobility', String())
    nurse_seniority = Column('nurse_seniority', String())
    enter_waiting_room = Column('enter_waiting_room', DateTime())
    leave_waiting_room = Column('leave_waiting_room', DateTime())
    nurse_begins_prep = Column('nurse_begins_prep', DateTime())
    begin_dialysis = Column('begin_dialysis', DateTime())
    end_dialysis = Column('end_dialysis', DateTime())
    nurse_applies_bandage = Column('nurse_applies_bandage', DateTime())
    enter_waiting_room_done = Column('enter_waiting_room_done', DateTime())
    leave_waiting_room_done = Column('leave_waiting_room_done', DateTime())

    def __init__(self):
        pass

    # def __init__(self, id, age, male, disabled, transport_type, ward_area, shift, vascular_access, mobility, nurse_seniority):
    #     self.id = id
    #     self.age = age
    #     self.male = male
    #     self.transport_type = transport_type
    #     self.ward_area = ward_area
    #     self.shift = shift
    #     self.vascular_access = vascular_access
    #     self.mobility = mobility
    #     self.nurse_seniority = nurse_seniority

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)