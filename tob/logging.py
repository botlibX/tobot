# This file is placed in the Public Domain.


"logging at level"


import logging


LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


datefmt = "%H:%M:%S"
format_short = "%(module).3s %(message)-76s"


class Formatter(logging.Formatter):

    def format(self, record):
        record.module = record.module.upper()
        return logging.Formatter.format(self, record)


def level(loglevel="debug"):
    if loglevel != "none":
        ch = logging.StreamHandler()
        formatter = Formatter(fmt=format_short, datefmt=datefmt)
        ch.setFormatter(formatter)
        logger = logging.getLogger()
        lvl = LEVELS.get(loglevel)
        if not lvl:
            return
        logger.setLevel(LEVELS.get(loglevel))
        logger.addHandler(ch)


def __dir__():
    return (
        'level',
   )
