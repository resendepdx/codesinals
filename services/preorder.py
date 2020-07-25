# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: services\preorder.py
# Compiled at: 2019-07-08 19:24:18
import time
from datetime import datetime, date, timedelta
from loguru import logger as B
import connection.APIConnection as A
from connection.RetryConnection import *
import models.Balance as C
from models.roboController import *
from services.tendencia import *

def buscaPayout(ativo, duracao):
    duracao = int(duracao)
    tenta = 0
    payoutDig = 0
    payoutBin = 0
    try:
        A.instance().connection.subscribe_strike_list(ativo, duracao)
        while 1:
            data = A.instance().connection.get_digital_current_profit(ativo, duracao)
            if data:
                payoutDig = int(data)
                break
            else:
                time.sleep(1)
                tenta += 1
            if tenta >= 10:
                break

        A.instance().connection.unsubscribe_strike_list(ativo, duracao)
    except Exception as inst:
        try:
            B.error(inst)
        finally:
            inst = None
            del inst

    try:
        data = A.instance().connection.get_all_profit()
        payout_tur = int(data[ativo]['turbo'] * 100)
        payout_bin = int(data[ativo]['binary'] * 100)
        if duracao >= 15:
            if payout_bin > 0:
                payoutBin = payout_bin
            else:
                payoutBin = payout_tur
        elif payout_tur > 0:
            payoutBin = payout_tur
        else:
            payoutBin = payout_bin
    except Exception as inst:
        try:
            pass
        finally:
            inst = None
            del inst

    return (
     payoutDig, payoutBin)


def ativoAberto(ativo, prioriDigital):
    aberto = False
    tipo = 'D'
    if prioriDigital:
        tipos = [
         'digital', 'turbo', 'binary']
    else:
        tipos = [
         'turbo', 'binary', 'digital']
    par = roboCtrl.instance().robo.ativosabertos
    if par == []:
        par = A.instance().connection.get_all_open_time()
        roboCtrl.instance().robo.ativosabertos = par
    for tpnome in tipos:
        if not aberto:
            for paridade in par[tpnome]:
                if paridade == ativo:
                    if par[tpnome][paridade]['open'] == True:
                        aberto = True
                        break

        if aberto:
            if tpnome == 'digital':
                tipo = 'D'
            else:
                tipo = 'B'
            break

    return (
     tipo, aberto)


def D(change_acc, viewTrend, qtdCandleTrend, trendEmaSma, priorid, operation):
    E = '0'
    if int(date.today().day) == int(operation.day):
        if VerifConnection():
            if change_acc:
                A.instance().connection.change_balance(A.instance().acc_type)
            Pdig, Pbin = buscaPayout(operation.pair, operation.expirationMode)
            if int(Pdig + Pbin) > 0:
                B.info('{} | {}M | Payout Digital: {} | Binary: {}', operation.pair, operation.expirationMode, Pdig, Pbin)
            prioriDigital = 1
            if operation.expirationMode > 15:
                prioriDigital = 0
            elif int(Pbin) > int(Pdig) and priorid == 0:
                prioriDigital = 0
            elif priorid == 1:
                prioriDigital = 1
            elif priorid == 2:
                prioriDigital = 0
            if prioriDigital:
                operation.payout = Pdig
            else:
                operation.payout = Pbin
            TipoAtivo = 'Digital'
            AtAberto = Idioma.traducao('Fechado')
            Tp, Ab = ativoAberto(operation.pair, prioriDigital)
            if Ab:
                operation.typepair = Tp
                AtAberto = Idioma.traducao('Aberto')
            if Tp == 'B':
                TipoAtivo = 'Binarias'
            if prioriDigital:
                if Tp == 'B':
                    operation.payout = Pbin
            elif Tp == 'D':
                operation.payout = Pdig
            B.info('{} | {} | {}', operation.pair, TipoAtivo, AtAberto)
            if not Ab or viewTrend and trendEmaSma:
                operation.trend, sq = getIndicadores(operation.pair, operation.expirationMode)
                if operation.trend != '':
                    B.info('{} | Tendência: {}', operation.pair, operation.trend)
                    B.info(sq)
                else:
                    B.info('{} | Tendência: {}', operation.pair, 'Sem resposta da IQ')
            else:
                operation.trend, sq = tendenciaCandles(operation.pair, operation.expirationMode, qtdCandleTrend)
                if operation.trend != '':
                    B.info('{} | Tendência: {} | {}', operation.pair, operation.trend, sq)
        else:
            msg = '{0} | {1}M | {2}'.format(operation.pair, operation.expirationMode, Idioma.traducao('Problema na conexão, verifique sua internet.'))
            B.error(msg)
            print(msg)