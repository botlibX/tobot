# This file is placed in the Public Domain.


import os


from tob.configs import Config
from tob.message import reply
from tob.package import get
from tob.utility import importer

def pth(event):
    mod = importer(f"{Config.name}.nucleus")
    if not mod:
        reply(event, "can't find web directory.")
        return
    path = os.path.join(mod.__path__[0], "index.html")
    reply(event, f"file://{path}")
