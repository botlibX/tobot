# This file is placed in the Public Domain.


import queue
import threading


from .brokers import add
from .handler import Handler
from .objects import keys


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.olock = threading.RLock()
        self.oqueue = queue.Queue()
        self.silent = True
        add(self)

    def announce(self, text):
        if not self.silent:
            self.raw(text)

    def display(self, event):
        with self.olock:
            for tme in sorted(keys(event.result)):
                self.dosay(
                           event.channel,
                           getattr(event.result, tme)
                          )

    def dosay(self, channel, text):
        self.say(channel, text)

    def raw(self, text):
        raise NotImplementedError("raw")

    def say(self, channel, text):
        self.raw(text)

    def wait(self):
        self.oqueue.join()


def __dir__():
    return (
        'Client',
   )
