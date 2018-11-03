import logging
import time

import boto3

from grts.events import Subscriber, subscribe
from grts.events.events import MetricEvent
from grts.sensors import W1TemperatureSensor, DigitalBooleanSensor


logger = logging.getLogger(__name__)


class Sensors:

    def __init__(self, *sensors):
        self.sensors = sensors

    def __iter__(self):
        return iter(self.sensors)

    def poll(self):
        while True:
            for sensor in self.sensors:
                logger.info("Reading sensor")
                sensor.read()
            logger.info("Sleeping 1 second")
            time.sleep(1)  # in seconds


SENSORS = Sensors(
    W1TemperatureSensor(name='temp0', serial='28-0213133348aa'),
    W1TemperatureSensor(name='temp1', serial='28-021313cde7aa'),
    DigitalBooleanSensor(name='liquid0', pin=5, invert=True)
)


class Data(Subscriber):
    last_readings = dict()

    @classmethod
    def handle(cls, event):
        cls.last_readings[event.dimensions['name']] = event


subscribe(Data, MetricEvent)


class CloudWatchPublisher(Subscriber):
    client = boto3.client('cloudwatch', region_name='us-west-1')

    @classmethod
    def handle(cls, event):
        cls.client.put_metric_data(
            MetricData=[
                event.serialize()
            ],
            Namespace=event.namespace
        )


subscribe(CloudWatchPublisher, MetricEvent)
