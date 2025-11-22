# This file is placed in the Public Domain.


from .objects import Object


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


def __dir__():
    return (
        'Default',
    )
