from model.DeviceClasses import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///../../wemo_db.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def get_devices():
    return session.query(Device).all()