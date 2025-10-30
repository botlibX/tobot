# This file is placed in the Public Domain.


"logging at level"


import logging as log


LEVELS = {
    'debug': log.DEBUG,
    'info': log.INFO,
    'warning': log.WARNING,
    'warn': log.WARNING,
    'error': log.ERROR,
    'critical': log.CRITICAL
}


datefmt = "%H:%M:%S"
format_short = "%(module).3s %(message)-76s"


class Formatter(log.Formatter):

    def format(self, record):
        record.module = record.module.upper()
        return log.Formatter.format(self, record)


def level(loglevel="debug"):
    if loglevel != "none":
        ch = log.StreamHandler()
        formatter = Formatter(fmt=format_short, datefmt=datefmt)
        ch.setFormatter(formatter)
        lvl = LEVELS.get(loglevel)
        if not lvl:
            return
        logger = log.getLogger()
        logger.setLevel(LEVELS.get(loglevel))
        logger.addHandler(ch)


def __dir__():
    return (
        'level',
   )
