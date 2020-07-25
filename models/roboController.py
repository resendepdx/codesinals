# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: models\roboController.py
# Compiled at: 2019-07-08 19:24:18
import threading
from datetime import datetime, date
from models.Traducao import *
from models.OperationCalc import *
Idioma = Traduzir()

class roboController(object):
    _roboController__instance = None
    _roboController__robo = None
    _roboController__view = 'console'
    _roboController__thr_conexao = None
    _roboController__thr_conexao: threading
    _roboController__listThread = []
    _roboController__dianoticias = 0
    _roboController__noticias = []
    operContrl = operController()

    @property
    def robo(self):
        return self._roboController__robo

    @robo.setter
    def robo(self, value):
        self._roboController__robo = value

    @property
    def view(self):
        return self._roboController__view

    @view.setter
    def view(self, value):
        self._roboController__view = value

    @property
    def thr_conexao(self):
        return self._roboController__thr_conexao

    @thr_conexao.setter
    def thr_conexao(self, value):
        self._roboController__thr_conexao = value

    @property
    def listThread(self):
        return self._roboController__listThread

    @listThread.setter
    def add_listThread(self, value):
        self._roboController__listThread.append(value)

    @property
    def dianoticias(self) -> date:
        return self._roboController__dianoticias

    @dianoticias.setter
    def dianoticias(self, value):
        self._roboController__dianoticias = value

    @property
    def noticias(self):
        return self._roboController__noticias

    @noticias.setter
    def add_noticias(self, value):
        self._roboController__noticias.append(value)

    @staticmethod
    def instance():
        if not roboController._roboController__instance:
            roboController._roboController__instance = roboController()
        return roboController._roboController__instance