# This file is placed in the Public Domain.


"client for a string"


class Fleet:

    clients = {}

    @staticmethod
    def add(client):
        Fleet.clients[repr(client)] = client

    @staticmethod
    def all():
        return Fleet.clients.values()

    @staticmethod
    def announce(txt):
        for client in Fleet.all():
            client.announce(txt)

    @staticmethod
    def display(evt):
        client = Fleet.get(evt.orig)
        client.display(evt)

    @staticmethod
    def get(orig):
        return Fleet.clients.get(orig, None)

    @staticmethod
    def like(orig):
        match = []
        for origin in Fleet.clients:
            if orig.split()[0] in origin.split()[0]:
                match.append(orig)
        return match

    @staticmethod
    def say(orig, channel, txt):
        client = Fleet.get(orig)
        client.say(channel, txt)

    @staticmethod
    def shutdown():
        for client in Fleet.all():
            client.wait()
            client.stop()


def __dir__():
    return (
        'Fleet',
   )
