from datetime import datetime
from typing import Any, Optional

import attr

__all__ = [
    'Event',
    'TemperatureEvent',
    'BooleanEvent'
]


@attr.s(frozen=True)
class Event:
    pass


@attr.s(frozen=True)
class MetricEvent(Event):
    metric_name = attr.ib(type=str)
    value = attr.ib(type=Any)
    unit = attr.ib(type=str, default='None')

    emitted_at = attr.ib(type=datetime, factory=datetime.now)
    dimensions = attr.ib(factory=dict, type=dict)
    namespace = attr.ib(default='Hydroponics/Sensors', type=str)

    def add_dimensions(self, **kwargs):
        self.dimensions.update(kwargs)

    def serialize(self):
        dimensions = [
            {
                'Name': name,
                'Value': value
            } for name, value in self.dimensions.items()
        ]
        return {
            'MetricName': self.metric_name,
            'Dimensions': dimensions,
            'Unit': self.unit,
            'Value': self.value
        }


@attr.s(frozen=True)
class TemperatureEvent(MetricEvent):
    pass


@attr.s(frozen=True)
class BooleanEvent(MetricEvent):
    pass
