# This file is placed in the Public Domain.


"write your own commands"


import inspect


from .brokers import getobj
from .methods import parse


"config"


class Cfg:

    def __getattr__(self, key):
        return self.__dict__.get(key, "")

    def __str__(self):
        return str(self.__dict__)


"commands"


class Commands:

    cmds = {}
    names = {}


def addcmd(*args):
    "add functions to commands."
    for func in args:
        name = func.__name__
        Commands.cmds[name] = func
        Commands.names[name] = func.__module__.split(".")[-1]


def getcmd(cmd):
    "get function for command."
    return Commands.cmds.get(cmd, None)
        

def scancmd(module):
    "scan a module for functions with event as argument."
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if 'event' not in inspect.signature(cmdz).parameters:
            continue
        addcmd(cmdz)


"callback"


def command(evt):
    "command callback."
    parse(evt, evt.text)
    func = getcmd(evt.cmd)
    if func:
        func(evt)
        bot = getobj(evt.orig)
        bot.display(evt)
    evt.ready()


"interface"


def __dir__():
    return (
        'Cfg',
        'Commands',
        'addcmd',
        'command',
        'getcmd',
        'scancmd'
    )
