# This file is placed in the Public Domain.


"write your own commands"


import importlib
import importlib.util
import inspect
import os
import sys


from .clients import Fleet
from .methods import parse
from .package import getmod, modules


class Config:

    level = "warn"
    name = os.path.dirname(__file__).split(os.sep)[-1]
    version = 137


class Commands:

    cmds = {}
    names = {}

    @staticmethod
    def add(*args):
        for func in args:
            name = func.__name__
            Commands.cmds[name] = func
            Commands.names[name] = func.__module__.split(".")[-1]

    @staticmethod
    def get(cmd):
        return Commands.cmds.get(cmd, None)


def command(evt):
    parse(evt, evt.txt)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        Fleet.display(evt)
    evt.ready()


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


def scanner(names=[]):
    for modname in modules():
        if modname.startswith("__"):
            continue
        if names and modname not in names:
            continue
        mod = getmod(modname)
        if mod:
            scan(mod)


def __dir__():
    return (
        'Comamnds',
        'command',
        'importer',
        'modules',
        'scan',
        'scanner',
        'table'
    )
