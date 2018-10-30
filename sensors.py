import abc
import os
import subprocess
import time
from logging import getLogger

logger = getLogger(__name__)


class Sensor(metaclass=abc.ABCMeta):

    MAX_LEN = 120

    def __init__(self, *name, id_=None):
        self.name = name
        self.id = id_ or hash(name)
        self.data = []

    def add_reading(self, value):
        if len(self.data) > self.MAX_LEN:
            self.data.pop(0)
        self.data.append(value)

    def cur_value(self):
        return self.data[-1]

    def average(self):
        return sum(self.data) / len(self.data)

    def max(self):
        return max(self.data)

    def min(self):
        return min(self.data)

    @abc.abstractmethod
    def read(self):
        pass


class W1TemperatureSensor(Sensor):

    DEVICE_BASE_DIR = '/sys/bus/w1/devices'
    DEVICE_FILE = 'w1_slave'

    def __init__(self, *, name, id_=None, serial):
        self.serial = serial
        super().__init__(name, id_)

    @property
    def device_file(self):
        return os.path.join(
            self.DEVICE_BASE_DIR, self.serial, self.DEVICE_FILE
        )

    def _read_temp(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _read_temp_proc(self):
        proc = subprocess.Popen(
            ['cat', self.device_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

    def read(self):
        lines = self._read_temp_proc()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_proc()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c