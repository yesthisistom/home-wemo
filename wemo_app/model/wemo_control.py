import pywemo
from suntime import Sun


def get_sunset_time(lat= 38.901658, lon=-77.038907):
    '''
    :param lat: incoming latitude
    :param lon: incoming longitude
    :return: returns the DateTime object of the sunset time as local to the computer requesting, not the coordinate
    '''
    sun = Sun(lat, lon)
    sunset = sun.get_local_sunset_time().replace(tzinfo=None)
    return sunset


def get_devices_on_network():
    return pywemo.discover_devices()


# def change_state(device_mac, state=0):
#     '''
#     :param device_name: device to change the state of, as a string
#     :param state: 0 for off, 1 for on.  Off by default
#     :return:
#     '''
#     device_list = [device for device in pywemo.discover_devices() if device.name == device_name]
#     if len(device_list) == 0:
#         print('Failed to find device on network:', device_name)
#         return False
#
#     device = device_list[0]
#     if device.get_state() != state:
#         device.toggle()
#
#     return True


# def get_device_state(device_name):
#     device_list = [device for device in pywemo.discover_devices() if device.name == device_name]
#     if len(device_list) == 0:
#         print('Failed to find device on network:', device_name)
#         return False
#
#     device = device_list[0]
#     return device.get_state()


