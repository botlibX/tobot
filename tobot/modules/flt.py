# This file is placed in the Public Domain.


from tob.brokers import Broker
from tob.methods import fmt
from tob.threads import name


def flt(event):
    if event.args:
        clts = Broker.all()
        index = int(event.args[0])
        if index < len(clts):
            event.reply(fmt(list(Broker.all())[index], empty=True))
        else:
            event.reply(f"only {len(clts)} clients in fleet.")
        return
    event.reply(' | '.join([name(o) for o in Broker.all()]))
