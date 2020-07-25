# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: services\ativosopen.py
# Compiled at: 2019-07-08 19:24:18
import time
from datetime import datetime
from loguru import logger as log
import connection.APIConnection as APIConnection
import models.roboController as roboCtrl
from models.ThreadOperacion import *

class AtivosAbertos:
    aguardarMinutos = 20
    executor = ThreadOper()

    def verif_ativos(self):
        while roboCtrl.instance().robo.iniciado:
            try:
                roboCtrl.instance().robo.ativosabertos = APIConnection.instance().connection.get_all_open_time()
                log.debug('Atualizou lista de ativos')
            except Exception as e:
                try:
                    log.error(e)
                finally:
                    e = None
                    del e

            time.sleep(60 * self.aguardarMinutos)

    def start_ativos(self):
        self.executor = ThreadOper(target=(self.verif_ativos), args=())
        roboCtrl.instance().add_listThread = self.executor
        self.executor.start()

    def stop_ativos(self):
        self.executor.stop()