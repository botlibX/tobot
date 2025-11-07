# This file is placed in the Public Domain.


"write your own commands"


import importlib
import importlib.util
import inspect
import os
import sys


from tob.clients import Fleet
from tob.objects import Object
from tob.threads import launch


class Mods:

    dirs = {}

    @staticmethod
    def add(name, path=None):
        if path is None:
            path = name
        Mods.dirs[name] = path


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


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")


def command(evt):
    parse(evt, evt.txt)
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        Fleet.display(evt)
    evt.ready()


def importer(name, pth):
    if not os.path.exists(pth):
        return
    spec = importlib.util.spec_from_file_location(name, pth)
    if not spec or not spec.loader:
        return
    mod = importlib.util.module_from_spec(spec)
    if not mod:
        return
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def inits(names):
    modz = []
    for name in names:
        for modname, path in Mods.dirs.items():
            modpath = os.path.join(path, name + ".py")
            if not os.path.exists(modpath):
                continue
        pkgname = path.split(os.sep)[-1]
        mname = ".".join((pkgname, name))
        mod = importer(mname, modpath)
        if mod and "init" in dir(mod):
            thr = launch(mod.init)
            modz.append((mod, thr))
    return modz


def modules():
    mods = []
    for name, path in Mods.dirs.items():
        if not os.path.exists(path):
            continue
        mods.extend([
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__")
        ])
    return sorted(mods)


def scan(module):
    for key, cmdz in inspect.getmembers(module, inspect.isfunction):
        if key.startswith("cb"):
            continue
        if 'event' in inspect.signature(cmdz).parameters:
            Commands.add(cmdz)


def scanner(names=[]):
    if not names:
        names = modules()
    for name in names:
        for modname, path in Mods.dirs.items():
            modpath = os.path.join(path, name + ".py")
            if not os.path.exists(modpath):
                continue
            pkgname = path.split(os.sep)[-1] or path
            mname = ".".join((pkgname, name))
            mod = importer(mname, modpath)
            if mod:
                scan(mod)


"utility"


def parse(obj, txt):
    data = {
        "args": [],
        "cmd": "",
        "gets": Default(),
        "index": None,
        "init": "",
        "opts": "",
        "otxt": txt,
        "rest": "",
        "silent": Default(),
        "sets": Default(),
        "txt": ""
    }
    for k, v in data.items():
        setattr(obj, k, getattr(obj, k, v))
    args = []
    nr = -1
    for spli in txt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "-=" in spli:
            key, value = spli.split("-=", maxsplit=1)
            setattr(obj.silent, key, value)
            setattr(obj.gets, key, value)
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            setattr(obj.sets, key, value)
            continue
        nr += 1
        if nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""


def __dir__():
    return (
        'Comamnds',
        'command',
        'importer',
        'modules',
        'scan',
        'scanner'
    )
