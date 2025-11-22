# This file is placed in the Public Domain.


import time


from tob.message import reply
from tob.objects import Object
from tob.persist import find, fntime, write
from tob.utility import elapsed


class Todo(Object):

    def __init__(self):
        Object.__init__(self)
        self.txt = ''


def dne(event):
    if not event.args:
        reply(event, "dne <txt>")
        return
    selector = {'txt': event.args[0]}
    nmr = 0
    for fnm, obj in find('todo', selector):
        nmr += 1
        obj.__deleted__ = True
        write(obj, fnm)
        reply(event, "ok")
        break
    if not nmr:
        reply(event, "nothing todo")


def tdo(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in find('todo', event.gets):
            lap = elapsed(time.time()-fntime(fnm))
            reply(event, f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            reply(event, "no todo")
        return
    obj = Todo()
    obj.txt = event.rest
    write(obj)
    reply(event, "ok")
