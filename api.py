import json

from flask import Blueprint

from .acquire import DATA, Sensor

sensors = Blueprint('sensors', __name__)


def serialize_sensor(sensor: Sensor):
    return {
        'name': sensor.name,
        'cur_value': sensor.cur_value(),
        'min': sensor.min(),
        'max': sensor.max(),
        'average': sensor.average()
    }


@sensors.route('/sensors')
def sensor_data():
    return json.dumps({
        'sensors': [
            serialize_sensor(sensor) for sensor in DATA.sensors
        ]
    })
