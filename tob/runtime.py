# This file is placed in the Public Domain.


"runtime"


import os


class Config:

    debug = False
    default = "irc,rss"
    init  = ""
    level = "warn"
    name = os.path.dirname(__file__).split(os.sep)[-1]
    opts = ""
    verbose = False
    version = 132


def __dir__():
    return (
        'Config',
    )
