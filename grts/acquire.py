import logging
import time

from grts.sensors import W1TemperatureSensor, DigitalBinarySensor

logger = logging.getLogger(__name__)


class Readings:

    def __init__(self, *sensors):
        self.sensors = sensors

    def poll(self):
        for sensor in self.sensors:
            reading = sensor.read()
            sensor.add_reading(reading)


SENSORS = [
    W1TemperatureSensor(name='temp1', serial='28-0213133348aa'),
    DigitalBinarySensor(name='liquid1', pin=5, invert=True)
]
DATA = Readings(*SENSORS)


def poll_sensors():
    while True:
        DATA.poll()
        time.sleep(1)  # in seconds
