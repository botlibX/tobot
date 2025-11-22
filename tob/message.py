# This file is placed in the Public Domain.


import threading
import time


from .default import Default
from .objects import Object


class Message(Default):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self.result = Object()
        self.kind = "event"


def ready(obj):
    obj._ready.set()


def reply(obj, text):
    setattr(obj.result, str(time.time()), text)


def wait(obj, timeout=None):
    obj._ready.wait()
    if obj._thr:
        obj._thr.join(timeout)


def __dir__():
    return (
        'Message',
        'ready',
        'reply',
        'wait'
   )
