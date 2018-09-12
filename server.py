import smbus
import time


BUS = smbus.SMBus(1)
ARDUINO_ADDR = 0x04


def write_number(value):
    BUS.write_byte(ARDUINO_ADDR, value)
    return -1


def read_number():
    number = BUS.read_byte(ARDUINO_ADDR)
    return number


while True:
    var = input("Enter 1 - 9: ")
    if not var:
        continue

        write_number(var)
    print("RPI: Hi Arduino, I sent you ", var)

    # sleep one second
    time.sleep(1)

    number = readNumber()
    print("Arduino: Hey RPI, I received a digit ", number)
