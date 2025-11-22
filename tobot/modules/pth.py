# This file is placed in the Public Domain.


import os


from tob.message import reply
from tob.package import get as mget


def pth(event):
    mod = mget("Config.name}.network")
    if not mod:
        reply(event, "can't find web directory.")
        return
    path = os.path.join(mod.__path__[0], "html", "index.html")
    reply(event, f"file://{path}")
