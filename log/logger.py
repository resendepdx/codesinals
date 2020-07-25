# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: log\logger.py
# Compiled at: 2019-07-08 19:24:18
import datetime, logging, os, sys
from loguru import logger as log
from log.path import PathLogs
logger = logging.getLogger()

def loguru_config():
    log_format = '[{time:DD-MM-YY HH:mm:ss}] <level>{message}</level>'
    log.remove()
    log.add((sys.stdout), format=log_format)
    log_name = '{time:DD-MM-YYYY}.log'
    log.add((os.path.join(PathLogs.logs_path, log_name)), format=log_format, encoding='utf-8')


def logging_config():
    formatter = logging.Formatter(fmt='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%d-%m-%y %H:%M:%S')
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


class LogConfig:

    def __init__(self):
        loguru_config()
        logging_config()


if __name__ == '__main__':
    pass