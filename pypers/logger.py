# Simple logger

import logging
import os

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVELS = {'critical': logging.CRITICAL,
              'error':    logging.ERROR,
              'warning':  logging.WARNING,
              'info':     logging.INFO,
              'debug':    logging.DEBUG,
              'notset':   logging.NOTSET}
DEFAULT_LEVEL = 'debug'


def logger_for(name, level=None):
    if level is None or level not in LOG_LEVELS:
        lvl = os.environ.get('PYPER_LOG_LEVEL', DEFAULT_LEVEL)
        level = LOG_LEVELS.get(lvl.lower(), DEFAULT_LEVEL)

    log = logging.getLogger(name)
    handler = logging.StreamHandler()  # log to stderr
    handler.setLevel(level)
    log.setLevel(level)
    handler.setFormatter(logging.Formatter(FORMAT))
    log.addHandler(handler)
    return log
