import logging

__all__ = [
    'Subscriber',
    'subscribe',
    'publish'
]


logger = logging.getLogger(__name__)


class Subscriber:

    def handle(self, event):
        raise NotImplementedError()


class EventBus:
    subscribers = {}

    @classmethod
    def publish(cls, event) -> None:
        event_type = type(event)
        for klass in event_type.__mro__:
            if klass in cls.subscribers:
                subscribers_for_type = cls.subscribers[klass]
                for subscriber in subscribers_for_type:
                    try:
                        subscriber.handle(event)
                    except Exception as e:
                        logger.warning(
                            "Exception when publishing to '%s': %s" %
                            (subscriber.__name__, e)
                        )

    @classmethod
    def subscribe(cls, subscriber, event_type):
        cls.subscribers.setdefault(event_type, []).append(subscriber)


subscribe = EventBus.subscribe
publish = EventBus.publish
