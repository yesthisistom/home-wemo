from model.wemo_control import *
from model.DeviceClasses import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_connection():
    engine = create_engine('sqlite:///../../wemo_db.db?' "check_same_thread=false")
    return sessionmaker(bind=engine)()


def get_devices():
    return get_connection().query(Device).all()


def get_device(dev_id, session=get_connection()):
    results = session.query(Device).filter(Device.id == dev_id)
    return results[0] if results else None


def get_activity(activity_id, session=get_connection()):
    results = session.query(DeviceActivity).filter(DeviceActivity.id == activity_id)[0]
    return results if results else None


def update_activity(activity_id, activityname, activitytime):
    session = get_connection()
    activity = get_activity(activity_id, session)
    if not activity:
        return False
    activity.activity_name = activityname
    activity.activity_time = activitytime

    session.add(activity)
    session.commit()
    session.close()

    return True


def delete_activity(activity_id):
    session = get_connection()
    session.query(DeviceActivity).filter(DeviceActivity.id == activity_id).delete()
    session.commit()
    session.close()


def add_activity(device_id, activityname, activitytime):
    session = get_connection()
    device = get_device(device_id, session)
    if not device:
        return False

    activity = DeviceActivity(activity_name=activityname, activity_time=activitytime)

    device.activities.append(activity)
    session.add(device)
    session.commit()
    session.close()

    return True

