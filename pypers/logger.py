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
DEFAULT_LEVEL = LOG_LEVELS['debug']


def logger_for(name, level=None):
    if level is None:
        lvl = os.environ.get('PYPER_LOG_LEVEL')
        if lvl is None:
            level = DEFAULT_LEVEL
        else:
            lvl = lvl.lower()
            if lvl in LOG_LEVELS:
                level = LOG_LEVELS[lvl]
            else:
                level = DEFAULT_LEVEL

    log = logging.getLogger(name)
    handler = logging.StreamHandler()  # log to stderr
    handler.setLevel(level)
    log.setLevel(level)
    handler.setFormatter(logging.Formatter(FORMAT))
    log.addHandler(handler)
    return log
