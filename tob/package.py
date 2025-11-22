# This file is placed in the Public Domain.


import os
import sys


from .utility import importer, spl


class Mods:

    dirs = {}
    ignore = []


def add(name, path):
    Mods.dirs[name] = path


def get(name):
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


def configure(name=None, ignore="", local=False):
    if name:
        pkg = importer(name)
        if pkg:
            add(name, pkg.__path__[0])
    if ignore:
        Mods.ignore = spl(ignore)
    if local:
        add("mods", "mods")


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
        'add',
        'get',
        'configure',
        'modules'
    )
