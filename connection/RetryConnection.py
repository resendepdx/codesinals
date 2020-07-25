# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: connection\RetryConnection.py
# Compiled at: 2019-07-08 19:24:18
import sys, time, os
from datetime import datetime
import PySimpleGUI as sg
from loguru import logger as log
import connection.APIConnection as APIConnection
import models.roboController as roboCtrl
from models.roboController import *
from models.ThreadOperacion import *
from services.noticias import *

def VerifConnection():
    error_password = '{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}'
    conOK = False
    verAtivos = False
    try:
        log.debug(Idioma.traducao('Verificando conexão...'))
        conOK = APIConnection.instance().connection.check_connect()
    except Exception as e:
        try:
            log.error('Erro de conexão com a IQ:')
            log.error(e)
        finally:
            e = None
            del e

    try:
        if not conOK:
            verAtivos = True
            log.debug(Idioma.traducao('Recuperando conexão...'))
            print(Idioma.traducao('Recuperando conexão...'))
            check, reason = APIConnection.instance().connection.connect()
            if check:
                log.warning(Idioma.traducao('Conexão recuperada.'))
                print(Idioma.traducao('Conexão recuperada.'))
                conOK = True
            elif reason == '[Errno -2] Name or service not known':
                log.error(Idioma.traducao('Problema na conexão, verifique sua internet.'))
                print(Idioma.traducao('Problema na conexão, verifique sua internet.'))
            elif reason == error_password:
                log.error(Idioma.traducao('Login/Senha inválido.'))
                print(Idioma.traducao('Login/Senha inválido.'))
        else:
            conOK = True
    except Exception as e:
        try:
            log.error(e)
        finally:
            e = None
            del e

    if conOK:
        if roboCtrl.instance().dianoticias != datetime.now().date():
            getNoticias()
        if verAtivos:
            roboCtrl.instance().robo.pesqAtviso.start_ativos()
    return conOK


class RetryConnection:
    first_check = 0

    def try_connection(self):
        while roboCtrl.instance().robo.iniciado:
            if self.first_check == 0:
                if roboCtrl.instance().dianoticias != datetime.now().date():
                    getNoticias()
                else:
                    try:
                        if not APIConnection.instance().connection.check_connect():
                            log.debug(Idioma.traducao('Recuperando conexão...'))
                            print(Idioma.traducao('Recuperando conexão...'))
                            APIConnection.instance().connection.connect()
                        server_time = APIConnection.instance().connection.get_server_timestamp()
                        local_time = time.time()
                        diff = local_time - server_time
                        self.first_check = diff
                        log.debug(Idioma.traducao('Diferenca de horario:') + ' {}s', round(diff, 3))
                        roboCtrl.instance().view.janela['-status-'].update(Idioma.traducao('Diferenca de horario:') + ' {0}s'.format(round(diff, 3)))
                        roboCtrl.instance().view.janela.Refresh()
                    except Exception as e:
                        try:
                            log.error(e)
                        finally:
                            e = None
                            del e

                    time.sleep(0.5)

    def verify_connection(self):
        if not roboCtrl.instance().thr_conexao:
            executor = ThreadOper(target=(self.try_connection), args=())
            roboCtrl.instance().thr_conexao = executor
            executor.start()