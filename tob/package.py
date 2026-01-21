# This file is placed in the Public Domain.


"module management"


import importlib.util
import os


from .command import scancmd
from .threads import launch
from .utility import spl


"modules"


class Mods:

    dirs = {}
    modules = {}


def initmods(name, path):
    Mods.dirs[name] = path


def getmods(ignore=""):
    "loop over modules."
    for pkgname, path in Mods.dirs.items():
        if not os.path.exists(path):
            continue
        for fnm in os.listdir(path):
            if fnm.startswith("__"):
                continue
            if not fnm.endswith(".py"):
                continue
            name = fnm[:-3]
            if ignore and name in spl(ignore):
                continue
            modname = f"{pkgname}.{name}"
            mod =  Mods.modules.get(modname, None)
            if not mod:
                mod = importer(modname, os.path.join(path, fnm))
            if mod:
                yield name, mod


def listmods(ignore=""):
    "comma seperated list of available modules."
    mods = []
    for pkgname, path in Mods.dirs.items():
        mods.extend([
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and
            not x.startswith("__") and
            x[:-3] not in spl(ignore)
        ])
    return ",".join(sorted(mods))


"utilities"


def importer(name, pth=""):
    "import module by path."
    if pth and os.path.exists(pth):
        spec = importlib.util.spec_from_file_location(name, pth)
    else:
        spec = importlib.util.find_spec(name)
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    if not mod:
        return None
    Mods.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


"runtime"


def inits(init, ignore="", wait=False):
    "scan named modules for commands."
    thrs = []
    for name, mod in getmods(ignore):
        if name not in spl(init):
            continue
        if "init" in dir(mod):
            thrs.append((name, launch(mod.init)))
    if wait:
        for name, thr in thrs:
            thr.join()
        

def scanner(ignore=""):
    "scan named modules for commands."
    res = []
    for name, mod in getmods(ignore):
        scancmd(mod)
        res.append((name, mod))
    return res


"interface"


def __dir__():
    return (
        'Mods',
        'initmods',
        'getmods',
        'importer',
        'inits',
        'listmods',
        'scanner'
    )
