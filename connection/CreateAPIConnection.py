# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: connection\CreateAPIConnection.py
# Compiled at: 2019-07-08 19:24:18
import sys
from loguru import logger as log
import os
from iqoptionapi.stable_api import IQ_Option
import connection.APIConnection as APIConnection
import models.Balance as Balance
import models.roboController as roboCtrl
from models.roboController import *

def apiconnect(user: str, passw: str):
    error_password = '{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}'
    apiconn = IQ_Option(user, passw)
    check, reason = apiconn.connect()
    if check == False:
        if reason == '[Errno -2] Name or service not known':
            log.error(Idioma.traducao('Problema na conexão, verifique sua internet.'))
            print(Idioma.traducao('Problema na conexão, verifique sua internet.'))
            roboCtrl.instance().view.janela['-status-'].update(Idioma.traducao('Problema na conexão, verifique sua internet.'))
            roboCtrl.instance().view.janela.Refresh()
        elif reason == error_password:
            log.error(Idioma.traducao('Login/Senha inválido.'))
            print(Idioma.traducao('Login/Senha inválido.'))
            roboCtrl.instance().view.janela['-status-'].update(Idioma.traducao('Login/Senha inválido.'))
            roboCtrl.instance().view.janela.Refresh()
        return
    return apiconn


def createapiconnection(user: str, passw: str, tp_conta: str):
    apiconn = apiconnect(user, passw)
    if apiconn:
        apiconn.change_balance(tp_conta)
        APIConnection.instance().connection = apiconn
        APIConnection.instance().acc_type = tp_conta
        balance = apiconn.get_balance()
        log.warning(Idioma.traducao('Conta conectada:') + ' {} | ' + Idioma.traducao('Saldo Atual $') + ' {}', apiconn.email, balance)
        print(Idioma.traducao('Conta conectada:'), apiconn.email)
        Balance.instance().balance = balance
        Balance.instance().actual_balance = balance
        Balance.instance().moeda = apiconn.get_currency()