# This file is placed in the Public Domain.


import os


from tob.defines import Config, where


def pth(event):
    fn = where(Config)
    path = os.path.join(fn, 'nucleus', "index.html")
    event.reply(f"file://{path}")
