import threading

from grts.acquire import SENSORS
from grts.api import sensors


def make_app():
    from flask import Flask

    app = Flask(__name__)
    app.register_blueprint(sensors)

    return app


def start_server():
    app = make_app()
    threading.Thread(target=app.run).start()
    SENSORS.poll()
