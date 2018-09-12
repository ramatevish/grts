from logging import getLogger
import smbus
import time


logger = getLogger(__name__)

BUS = smbus.SMBus(1)
ARDUINO_ADDR = 0x04
SENSORS = [
    (0x01, 'temperature')
]


class Signals(object):
    START = 0
    END = 1
    SEND_SENSOR_DATA = 2


def send_signal(signal):
    BUS.write_byte(ARDUINO_ADDR, signal)
    return -1


def read_byte():
    number = BUS.read_byte(ARDUINO_ADDR)
    return number


class Sensor(object):

    MAX_LEN = 120

    def __init__(self, address, name):
        self.address = address
        self.name = name
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


class Readings(object):

    def __init__(self, *sensors):
        self.sensors = {
            sensor.address: sensor for sensor in sensors
        }

    def add_sensor_reading(self, address, reading):
        try:
            sensor = self.sensors[address]
        except KeyError:
            logger.warning("Couldn't find sensor w/ address %s" % address)
            return

        sensor.add_reading(reading)


DATA = Readings(
    *(Sensor(*args) for args in SENSORS)
)


def poll_sensors():
    while True:
        send_signal(Signals.START)
        send_signal(Signals.SEND_SENSOR_DATA)

        # TODO(ramatevish) read more than one sensor
        addr = read_byte()
        meta = read_byte()
        data1 = read_byte()
        data2 = read_byte()

        # TODO(ramatevish) handle metadata and second data byte
        DATA.add_sensor_reading(addr, data1)

        send_signal(Signals.END)

        time.sleep(1)  # in seconds
