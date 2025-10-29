# This file is placed in the Public Domain.


"runtime"


import inspect
import os
import pathlib
import sys
import time


from .clients import Client
from .command import Commands, Config, command, table
from .handler import Event
from .logging import level
from .package import Mods, inits, modules, sums
from .persist import Workdir, moddir, pidname, skel
from .utility import parse, spl


CHECKSUM = "74c8e52fc1ef4d1f5dc90eae4f2200c4"


"in the beginning"


def boot(doparse=True):
    if doparse:
        parse(Config, " ".join(sys.argv[1:]))
        Config.level = Config.sets.level or Config.level
    Workdir.wdr = Workdir.wdr or os.path.expanduser(f"~/.{Config.name}")
    level(Config.level)
    if "a" in Config.opts:
        Config.sets.init = ",".join(modules())
    skel()
    table()
    sums(CHECKSUM)


"scripts"


def background(clt):
    daemon("-v" in sys.argv)
    privileges()
    boot(False)
    pidfile(pidname(Config.name))
    inits(spl(Config.default))
    forever()


def console(clt):
    import readline # noqa: F401
    boot()
    for _mod, thr in inits(spl(Config.sets.init)):
        if "w" in Config.opts:
            thr.join(30.0)
    csl = clt()
    csl.start()
    forever()


def control(clt):
    if len(sys.argv) == 1:
        return
    boot()
    csl = clt()
    evt = Event()
    evt.orig = repr(csl)
    evt.type = "command"
    evt.txt = " ".join(sys.argv[1:])
    evt.cmd  = evt.txt.split()[0]
    command(evt)
    evt.wait()


def service(clt):
    privileges()
    boot(False)
    pidfile(pidname(Config.name))
    inits(spl(Config.default))
    forever()


"utility"


def check(txt):
    args = sys.argv[1:]
    for arg in args:
        if not arg.startswith("-"):
            continue
        for char in txt:
            if char in arg:
                return True
    return False


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


def wrapped(func, clt):
    try:
        func(clt)
    except (KeyboardInterrupt, EOFError):
        pass


def wrap(func, clt):
    import termios
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        wrapped(func, clt)
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def __dir__():
    return (
        'background',
        'boot',
        'console',
        'control',
        'daemon',
        'forever',
        'pidfile',
        'privileges',
        'service',
        'wrap',
        'wrapped'
    )
