from flask import Blueprint, jsonify

from .acquire import Data

sensors = Blueprint('sensors', __name__)


@sensors.route('/sensors')
def sensor_data():
    return jsonify({
        'sensors': [
            event.serialize() for event in Data.last_readings.values()
        ]
    })
