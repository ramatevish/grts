import threading

from acquire import poll_sensors
from api import sensors


def make_app():
    from flask import Flask

    app = Flask(__name__)
    app.register_blueprint(sensors)


def start_server():
    app = make_app()
    threading.Thread(target=poll_sensors).start()
    app.run()


if __name__ == '__main__':
    start_server()
