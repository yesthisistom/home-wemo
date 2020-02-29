import time
import traceback
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
sys.path.insert(1, './wemo_app')
from model import *


def run_wemo_check():
    engine = create_engine('sqlite:///../database/wemo_db.db', echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    devices = session.query(Device).all()
    for device in devices:
        for activity in device.activities:
            try:
                activity_time = activity.get_day_occurence()

                if activity_time < datetime.now() and (datetime.now() - activity_time).seconds / 60 < 15:
                    print('activity found')
                    device.change_state(activity.turn_on)
            except:            
                print('Activity Failed For', activity.activity_name)


print(__name__)
## Main loop execution
if __name__ == '__main__':

    pause_time_mins = 5
    print("starting loop")
    while True:
        try:
            run_wemo_check()

        except Exception as e:
            print(e)
            traceback.print_exc()

        time.sleep(pause_time_mins*60)

