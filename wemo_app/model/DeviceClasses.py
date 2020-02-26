import pywemo
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    mac = Column(String)
    name = Column(String)
    description = Column(String)
    ip_address = Column(String)

    activities = relationship("DeviceActivity", lazy='subquery', back_populates='devices', cascade="all, delete, delete-orphan")

    wemo_device = None

    def __repr__(self):
        return "<User(name='%s', desc='%s')>" % (self.name, self.description)

    def _get_device(self):
        if self.wemo_device:
            return True

        ip_address = self.ip_address
        port = pywemo.ouimeaux_device.probe_wemo(ip_address)
        if not port:
            return None
        url = 'http://%s:%i/setup.xml' % (ip_address, port)
        self.wemo_device = pywemo.discovery.device_from_description(url, None)

        return True

    def is_powered_on(self):
        # TEMP
        # return None
        self._get_device()
        if not self.wemo_device:
            return None

        return self.wemo_device.get_state()

    def change_state(self, turn_on=False):
        self._get_device()
        if not self.wemo_device:
            return None

        # TODO: See if these return a status, and return that?
        return self.wemo_device.on() if turn_on else self.wemo_device.off()


class DeviceActivity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    activity_name = Column(String, nullable=False)
    activity_time = Column(String, nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'))
    devices = relationship("Device", back_populates="activities", lazy='subquery')

    def __repr__(self):
        return "<DeviceActivity(activity_name='%s')>" % self.activity_name

