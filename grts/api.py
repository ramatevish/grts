from flask import Blueprint, jsonify

from .acquire import DATA

sensors = Blueprint('sensors', __name__)


def serialize_sensor(sensor):
    return {
        'name': sensor.name,
        'cur_value': sensor.cur_value(),
        'min': sensor.min(),
        'max': sensor.max(),
        'average': sensor.average()
    }


@sensors.route('/sensors')
def sensor_data():
    return jsonify({
        'sensors': [
            serialize_sensor(sensor) for sensor in DATA.sensors
        ]
    })
