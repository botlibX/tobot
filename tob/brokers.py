# This file is placed in the Public Domain.


from .objects import Object, values


class Broker:

    objects = Object()


def add(obj):
    setattr(Broker.objects, repr(obj), obj)


def get(origin):
    return getattr(Broker.objects, origin, None)


def all(attr=None):
    for obj in values(Broker.objects):
        if attr and attr not in dir(obj):
            continue
        yield obj


def like(origin):
    for orig in Broker.objects:
        if origin.split()[0] in orig.split()[0]:
            yield orig


def __dir__():
    return (
        'Broker',
        'add',
        'get',
        'all',
        'like'
    )
