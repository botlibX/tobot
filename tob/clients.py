# This file is placed in the Public Domain.


"clients"


import queue
import threading


from typing import Any, Generator, List, ValuesView


from tob.handler import Handler
from tob.objects import Object, values
from tob.threads import launch


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.olock = threading.RLock()
        self.oqueue = queue.Queue()
        self.silent = True
        Fleet.add(self)

    def announce(self, text) -> None:
        if not self.silent:
            self.raw(text)

    def display(self, event) -> None:
        with self.olock:
            for tme in sorted(event.result):
                self.dosay(
                           event.channel,
                           event.result[tme]
                          )

    def dosay(self, channel, text) -> None:
        self.say(channel, text)

    def raw(self, text) -> None:
        raise NotImplementedError("raw")

    def say(self, channel, text) -> None:
        self.raw(text)

    def wait(self) -> None:
        self.oqueue.join()    


class Output(Client):

    def output(self) -> None:
        while True:
            event = self.oqueue.get()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def start(self) -> None:
        launch(self.output)
        super().start()

    def stop(self) -> None:
        self.oqueue.put(None)
        super().stop()


class Fleet:

    clients = Object()

    @staticmethod
    def add(client) -> None:
        setattr(Fleet.clients, repr(client), client)

    @staticmethod
    def all() -> ValuesView[Any]:
        return values(Fleet.clients)

    @staticmethod
    def announce(text) -> None:
        for client in Fleet.all():
            client.announce(text)

    @staticmethod
    def display(event) -> None:
        client = Fleet.get(event.orig)
        if client:
            client.display(event)

    @staticmethod
    def get(origin) -> Client | None:
        return getattr(Fleet.clients, origin, None)

    @staticmethod
    def like(origin) -> Generator[Client]:
        for orig in Fleet.clients:
            if origin.split()[0] in orig.split()[0]:
                yield orig

    @staticmethod
    def say(orig, channel, txt) -> None:
        client = Fleet.get(orig)
        if client:
            client.say(channel, txt)

    @staticmethod
    def shutdown() -> None:
        for client in Fleet.all():
            client.wait()
            client.stop()


class Pool:

    clients: List[Client] = []
    lock = threading.RLock()
    nrcpu = 1
    nrlast = 0

    @staticmethod
    def add(client) -> None:
        Pool.clients.append(client)

    @staticmethod
    def init(cls, nr, verbose=False) -> None:
        Pool.nrcpu = nr
        for _x in range(Pool.nrcpu):
            clt = cls()
            clt.start()
            Pool.add(clt)

    @staticmethod
    def put(event) -> None:
        with Pool.lock:
            if Pool.nrlast >= Pool.nrcpu-1:
                Pool.nrlast = 0
            clt = Pool.clients[Pool.nrlast]
            clt.put(event)
            Pool.nrlast += 1



def __dir__():
    return (
        'Client',
        'Fleet',
        'Output'
   )
