# This file is placed in the Public Domain.


import time


from tob.message import reply
from tob.utility import elapsed


STARTTIME = time.time()


def upt(event):
    reply(event, elapsed(time.time()-STARTTIME))
