# This file is placed in the Public Domain.


"handle events"


import queue
import threading
import time


from tob.objects import Object
from tob.threads import launch


class Event:

    def __init__(self):
        self._ready = threading.Event()
        self._thr = None
        self.channel = ""
        self.ctime = time.time()
        self.orig = ""
        self.result = {}
        self.text = ""
        self.type = "event"

    def ready(self) -> None:
        self._ready.set()

    def reply(self, text) -> None:
        self.result[time.time()] = text

    def wait(self, timeout=None) -> None:
        self._ready.wait()
        if self._thr:
            self._thr.join(timeout)


class Handler:

    def __init__(self):
        self.cbs = Object()
        self.queue = queue.Queue()

    def callback(self, event) -> None:
        func = getattr(self.cbs, event.type, None)
        if func:
            name = event.text and event.text.split()[0]
            event._thr = launch(func, event, name=name)
        else:
            event.ready()

    def loop(self) -> None:
        while True:
            event = self.poll()
            if event is None:
                break
            event.orig = repr(self)
            self.callback(event)

    def poll(self) -> Event:
        return self.queue.get()

    def put(self, event) -> None:
        self.queue.put(event)

    def register(self, type, callback) -> None:
        setattr(self.cbs, type, callback)

    def start(self) -> None:
        launch(self.loop)

    def stop(self) -> None:
        self.queue.put(None)


def __dir__():
    return (
        'Event',
        'Handler'
   )
