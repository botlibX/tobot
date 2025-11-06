# This file is placed in the Public Domain.


"module management"


import importlib
import importlib.util
import inspect
import logging
import os
import sys
import threading
import _thread


from .threads import launch
from .persist import Workdir, moddir


lock = threading.RLock()


class Mods:

    dirs = {}

    @staticmethod
    def add(name, path):
        Mods.dirs[name] = path


def getmod(name):
    for nme, path in Mods.dirs.items():
        mname = nme + "." +  name
        module = sys.modules.get(mname, None)
        if module:
            return module
        pth = os.path.join(path, f"{name}.py")
        if not os.path.exists(pth):
            continue
        mod = importer(mname, pth)
        if mod:
            return mod


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
    for name in modules():
        if name not in names:
            continue
        module = getmod(name)
        if module and "init" in dir(module):
            thr = launch(module.init)
            modz.append((module, thr))
    return modz


def modules():
    mods = []
    for name, path in Mods.dirs.items():
        print(path)
        if not os.path.exists(path):
            continue
        mods.extend([
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__")
           ])
    print(mods)
    return sorted(mods)


def __dir__():
    return (
        'Mods',
        'getmod',
        'importer',
        'inits',
        'md5sum',
        'modules'
    )
