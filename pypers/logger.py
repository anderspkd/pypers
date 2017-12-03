# Simple logger

import logging

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def logger_for(name, level=logging.DEBUG):
    log = logging.getLogger(name)
    handler = logging.StreamHandler()  # log to stderr
    handler.setLevel(level)
    log.setLevel(level)
    handler.setFormatter(logging.Formatter(FORMAT))
    log.addHandler(handler)
    return log
