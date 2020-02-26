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

    def __repr__(self):
        return "<User(name='%s', desc='%s')>" % (self.name, self.description)


class DeviceActivity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    activity_name = Column(String, nullable=False)
    activity_time = Column(String, nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'))
    devices = relationship("Device", back_populates="activities")

    def __repr__(self):
        return "<DeviceActivity(activity_name='%s')>" % self.activity_name

