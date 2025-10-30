# This file is placed in the Public Domain.


"runtime"


import inspect
import os
import pathlib
import sys
import time


from .command import parse, table
from .logging import level
from .package import Mods, modules, sums
from .persist import Workdir, moddir, skel


STARTTIME = time.time()


class Config:

    debug = False
    default = "irc,rss"
    init  = ""
    level = "warn"
    name = os.path.dirname(__file__).split(os.sep)[-1]
    opts = ""
    verbose = False
    version = 132


def boot(mods, checksum, doparse=True):
    Mods.add("modules", os.path.dirname(inspect.getfile(mods)))
    Mods.add("mods", moddir())
    if doparse:
        parse(Config, " ".join(sys.argv[1:]))
        Config.level = Config.sets.level or Config.level
    Workdir.wdr = Workdir.wdr or os.path.expanduser(f"~/.{Config.name}")
    level(Config.level)
    if "a" in Config.opts:
        Config.sets.init = ",".join(modules())
    skel()
    table()
    sums(checksum)


def daemon(verbose=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    os.nice(10)


def forever():
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            break


def pidfile(filename):
    if os.path.exists(filename):
        os.unlink(filename)
    path2 = pathlib.Path(filename)
    path2.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges():
    import getpass
    import pwd
    pwnam2 = pwd.getpwnam(getpass.getuser())
    os.setgid(pwnam2.pw_gid)
    os.setuid(pwnam2.pw_uid)


def wrapped(func):
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass


def wrap(func):
    import termios
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        wrapped(func)
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def __dir__():
    return (
        'STARTTIME',
        'Config',
        'boot',
        'daemon',
        'forever',
        'pidfile',
        'privileges',
        'wrap',
        'wrapped'
    )
