# This file is placed in the Public Domain.


import importlib
import importlib.util
import os
import sys


class Mods:

    dirs: dict[str, str] = {}
    ignore: list[str] = []

    def add(name, path=None):
        if path is None:
            path = name
        Mods.dirs[name] = path


def getmod(name):
    mname = ""
    pth = ""
    if name in Mods.ignore:
        return
    for packname, path in Mods.dirs.items():
        modpath = os.path.join(path, name + ".py")
        if os.path.exists(modpath):
            pth = modpath
            mname = f"{packname}.{name}"
            break
    return sys.modules.get(mname, None) or importer(mname, pth)


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


def modules():
    mods = []
    for name, path in Mods.dirs.items():
        if name in Mods.ignore:
            continue
        if not os.path.exists(path):
            continue
        mods.extend([
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__") and x not in Mods.ignore
        ])
    return sorted(mods)


def __dir__():
    return (
        'Mods',
        'getmod',
        'importer',
        'modules',
    )
