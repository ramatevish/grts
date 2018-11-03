import abc
import os
import re
import subprocess

from grts import events
from grts.events import TemperatureEvent, BooleanEvent

try:
    import RPi.GPIO as gpio
except ImportError:
    # TODO(ramatevish): add mock for testing
    pass
import logging


logger = logging.getLogger(__name__)


class Sensor(metaclass=abc.ABCMeta):

    def __init__(self, *, name, id_=None):
        self.name = name
        self.id = id_ or hash(name)

    @abc.abstractmethod
    def _get_reading(self):
        pass

    @abc.abstractmethod
    def _publish_event(self, reading):
        pass

    def read(self):
        reading = self._get_reading()
        if reading is not None:
            self._publish_event(reading)
        return reading


class DigitalBooleanSensor(Sensor):

    def __init__(self, *, name, id_=None, pin, pull_up_down=None, invert=False):
        self.pin = pin
        self.pull_up_down = pull_up_down
        self.invert = invert
        self._ready = False
        super().__init__(name=name, id_=id_)

    def _setup_pin(self):
        gpio.setmode(gpio.BCM)

        # Do this here so construction of sensor doesn't throw errors in non-pi envs
        pull_up_down = self.pull_up_down
        if pull_up_down is None:
            pull_up_down = gpio.PUD_DOWN

        gpio.setup(self.pin, gpio.IN, pull_up_down=pull_up_down)
        self._ready = True

    def _get_reading(self):
        if not self._ready:
            self._setup_pin()
        reading = gpio.input(self.pin) == 1.0
        if self.invert:
            reading = not reading
        return reading

    def _publish_event(self, reading):
        event = BooleanEvent(
            metric_name=self.name,
            value=reading,
            dimensions=dict(
                unit='Boolean',
                name=self.name
            )
        )
        events.publish(event)


class W1TemperatureSensor(Sensor):

    DEVICE_BASE_DIR = '/sys/bus/w1/devices'
    DEVICE_FILE = 'w1_slave'

    def __init__(self, *, name, id_=None, serial):
        self.serial = serial
        super().__init__(name=name, id_=id_)

    @property
    def device_file(self):
        return os.path.join(
            self.DEVICE_BASE_DIR, self.serial, self.DEVICE_FILE
        )

    def _read_temp_file(self):
        proc = subprocess.Popen(
            ['cat', self.device_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        out_decode = out.decode('utf-8')
        return out_decode

    def _get_reading(self):
        lines = self._read_temp_file()
        reading = re.search(r'.*(YES)\n.*t=(\d+)', lines)
        if reading is not None:
            return float(reading.group(2)) / 1000.0

    def _publish_event(self, reading):
        event = TemperatureEvent(
            metric_name=self.name,
            value=reading,
            dimensions=dict(
                unit='Celsius',
                name=self.name,
                serial=self.serial
            )
        )
        events.publish(event)
