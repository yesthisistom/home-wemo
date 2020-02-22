from model.wemo_control import *
from model.DeviceClasses import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_connection():
    engine = create_engine('sqlite:///../../wemo_db.db', echo=True)
    return sessionmaker(bind=engine)()


def get_devices():
    return get_connection().query(Device).all()