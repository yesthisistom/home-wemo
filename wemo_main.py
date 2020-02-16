import json
import time
import pywemo
import traceback
import pandas as pd
from suntime import Sun
from datetime import datetime

print("Start")

def get_sunset_time(lat= 38.901658, lon=-77.038907):
    '''
    :param lat: incoming latitude
    :param lon: incoming longitude
    :return: returns the DateTime object of the sunset time as local to the computer requesting, not the coordinate
    '''
    sun = Sun(lat, lon)
    sunset = sun.get_local_sunset_time().replace(tzinfo=None)
    return sunset


def change_state(device_name, state=0):
    '''
    :param device_name: device to change the state of, as a string
    :param state: 0 for off, 1 for on.  Off by default
    :return:
    '''
    device_list = [device for device in pywemo.discover_devices() if device.name == device_name]
    if len(device_list) == 0:
        print('Failed to find device on network:', device_name)
        return False

    device = device_list[0]
    if device.get_state() != state:
        device.toggle()

    return True


def parse_activity_time(time_str):
    if time_str.lower() == 'sunset':
        return get_sunset_time()

    return pd.to_datetime(time_str).to_pydatetime()


def run_wemo_check():
    json_file = 'wemo_json.json'
    with open(json_file) as rdr:
        config = json.load(rdr)

    for activity in config:
        activity_time = parse_activity_time(activity['time'])
        print(activity_time)
        print('timedelta: ', datetime.now() - activity_time)

        if activity_time < datetime.now() and (datetime.now() - activity_time).seconds / 60 < 15:
            print('activity found')
            change_state(activity['name'], 0 if activity['event'] == 'turn off' else 1)

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

