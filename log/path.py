# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: log\path.py
# Compiled at: 2019-07-08 19:24:18
import os
from loguru import logger as log
from pathlib import Path

class PathLogs:
    """dir"""
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'temp')
    logs_path = os.path.abspath(os.path.join(base_path, 'logs'))
    lib_logs_path = os.path.abspath(os.path.join(base_path, 'logs'))

    @staticmethod
    def create_dirs():
        PathLogs.create_log()
        PathLogs.create_lib_logs()

    @staticmethod
    def create_bin():
        PathLogs.create_dir(PathLogs.bin)

    @staticmethod
    def create_log():
        PathLogs.create_dir(PathLogs.logs_path)

    @staticmethod
    def create_lib_logs():
        PathLogs.create_dir(PathLogs.lib_logs_path)

    @staticmethod
    def create_dir(path):
        try:
            os.makedirs(path, exist_ok=True)
        except OSError:
            log.debug('Creation of the directory %s failed' % path)