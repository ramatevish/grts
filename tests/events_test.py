from unittest.mock import MagicMock

import pytest

from grts.events import *


def make_listener():
    class MyListener(Subscriber):
        pass

    listener = MyListener()
    listener.handle = MagicMock()


@pytest.fixture()
def listener():
    return make_listener()


def test_pub_sub_simple(listener):
    event = Event()

    subscribe(listener, Event)
    publish(event)

    listener.handle.assert_called_once_with(event)


def test_pub_sub_subclass(listener):

    class MyEvent(Event):
        pass

    subscribe(listener, MyEvent)

    event = Event()
    publish(event)
    listener.handle.assert_not_called()

    event = MyEvent()
    publish(event)
    listener.handle.assert_called_once_with(event)


def test_pub_sub_multiple():
    l1, l2 = make_listener(), make_listener()

    class MyEvent(Event):
        pass

    subscribe(l1, Event)
    subscribe(l2, MyEvent)

    event = object()
    publish(event)
    l1.handle.assert_not_called()
    l2.handle.assert_not_called()

    event = Event()
    publish(event)
    l1.handle.assert_called_once_with(event)
    l2.handle.assert_not_called()
    l1.handle.reset_mock()

    event = MyEvent()
    publish(event)
    l1.handle.assert_called_once_with(event)
    l2.handle.assert_called_once_with(event)
