# This file is placed in the Public Domain.


from tob.message import reply
from tob.package import modules


def mod(event):
    reply(event, ",".join(modules()))
