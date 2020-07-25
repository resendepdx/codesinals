# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: connection\APIConnection.py
# Compiled at: 2019-07-08 19:24:18
import sys, os
from iqoptionapi.stable_api import IQ_Option

class APIConnection(object):
    _APIConnection__instance = None
    _APIConnection__connection = None
    _APIConnection__connection: IQ_Option
    _APIConnection__acc_type: str

    @property
    def connection(self):
        return self._APIConnection__connection

    @connection.setter
    def connection(self, value):
        self._APIConnection__connection = value

    @property
    def acc_type(self):
        return self._APIConnection__acc_type

    @acc_type.setter
    def acc_type(self, value):
        self._APIConnection__acc_type = value

    @staticmethod
    def instance():
        if not APIConnection._APIConnection__instance:
            APIConnection._APIConnection__instance = APIConnection()
        return APIConnection._APIConnection__instance