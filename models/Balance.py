# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: models\Balance.py
# Compiled at: 2019-07-08 19:24:18
import schedule as H
import models.sorosgale as sorosgale

class Balance(object):
    _Balance__instance = None
    _Balance__moeda = 'BRL'
    _Balance__start_balance = 0
    _Balance__start_balance: float
    _Balance__actual_balance = 0
    _Balance__actual_balance: float
    _Balance__win_limit = 0
    _Balance__win_limit: float
    _Balance__stop_limit = 0
    _Balance__stop_limit: float
    _Balance__sorosgale: None

    @property
    def moeda(self):
        return self._Balance__moeda

    @moeda.setter
    def moeda(self, value):
        self._Balance__moeda = value

    @property
    def balance(self):
        return self._Balance__start_balance

    @balance.setter
    def balance(self, value):
        self._Balance__start_balance = value

    @property
    def actual_balance(self):
        return self._Balance__actual_balance

    @actual_balance.setter
    def actual_balance(self, value):
        self._Balance__actual_balance = value

    @property
    def win_limit(self):
        return self._Balance__win_limit

    @win_limit.setter
    def win_limit(self, value):
        self._Balance__win_limit = value

    @property
    def stop_limit(self):
        return self._Balance__stop_limit

    @stop_limit.setter
    def stop_limit(self, value):
        self._Balance__stop_limit = value

    @property
    def sorosgale(self):
        return self._Balance__sorosgale

    @sorosgale.setter
    def sorosgale(self, value):
        self._Balance__sorosgale = value

    @staticmethod
    def instance():
        if not Balance._Balance__instance:
            Balance._Balance__instance = Balance()
            Balance._Balance__sorosgale = sorosgale()
        return Balance._Balance__instance