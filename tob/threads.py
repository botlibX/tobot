# This file is placed in the Public Domain.


"run non-blocking"


import logging
import queue
import threading
import time
import _thread


from tob.utility import name


class Thread(threading.Thread):

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.name = kwargs.get("name", name(func))
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def join(self, timeout=None):
        result = None
        try:
            super().join(timeout)
            result = self.result
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        return result

    def run(self):
        func, args = self.queue.get()
        try:
            self.result = func(*args)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


def launch(func, *args, **kwargs):
    thread = Thread(func, *args, **kwargs)
    thread.start()
    return thread


def __dir__():
    return (
        'Thread',
        'launch'
   )
