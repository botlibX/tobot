# This file is placed in the Public Domain.


"logging at level"


import logging 


LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


datefmt = "%H:%M:%S"
format_short = "%(module).3s %(message).76s"


class Formatter(logging.Formatter):

    def format(self, record):
        record.module = record.module.upper()
        return logging.Formatter.format(self, record)


def level(loglevel="debug"):
    if loglevel != "none":
        lvl = LEVELS.get(loglevel)
        if not lvl:
            return
        logger = logging.getLogger()
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.setLevel(lvl)
        formatter = Formatter(format_short, datefmt=datefmt)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)


def __dir__():
    return (
        'level',
   )
