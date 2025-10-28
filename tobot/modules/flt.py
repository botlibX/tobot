# This file is placed in the Public Domain.


from tob.brokers import Fleet
from tob.utility import fmt, name


def flt(event):
    if event.args:
        clts = Fleet.all()
        index = int(event.args[0])
        if index < len(clts):
            event.reply(fmt(list(Fleet.all())[index], empty=True))
        else:
            event.reply(f"only {len(clts)} clients in fleet.")
        return
    event.reply(' | '.join([name(o) for o in Fleet.all()]))