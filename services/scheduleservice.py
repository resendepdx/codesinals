# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: services\scheduleservice.py
# Compiled at: 2019-07-08 19:24:18
import time
from datetime import datetime, timedelta
import schedule as B
from loguru import logger as D
import log.path as P
import models.OperationProgrammed as E
import models.roboController as roboCtrl
from models.roboController import *
from connection.RetryConnection import *
import services.preorder as F
import services.buyservice as G
import services.sendmsg as HL

def C(operations):
    FT = '%H:%M:%S'
    FD = '%d/%m/%y %H:%M:%S'
    roboCtrl.instance().operContrl.agenda = E.G(operations, roboCtrl.instance().robo.delay)
    B.clear()
    for A in roboCtrl.instance().operContrl.agenda:
        dhexpira = A.expirationDate - timedelta(seconds=35)
        B.every().days.at(A.programmedHour.strftime(FT)).do(G().dooperation, A).tag('agendaID' + str(A.op_id))
        D.info('ID {}: {} | {} | {} | {}M', A.op_id, A.programmedHour.strftime(FD), A.pair, A.direction.upper(), A.expirationMode)
        B.every().days.at(A.pre_order.strftime(FT)).do(F.D, roboCtrl.instance().robo.manterConta, roboCtrl.instance().robo.tendusar, roboCtrl.instance().robo.tendvelas, roboCtrl.instance().robo.tendemasma, roboCtrl.instance().robo.priorid, A).tag('agendaPreID' + str(A.op_id))
        B.every().days.at(dhexpira.strftime(FT)).do(VerifConnection).tag('agendaCnxID' + str(A.op_id))


def cancel(id):
    try:
        for sinal in roboCtrl.instance().operContrl.agenda:
            if not sinal.situacao == Idioma.traducao('Aguardando'):
                if sinal.situacao == Idioma.traducao('Agendado'):
                    pass
            cancelId(sinal.op_id)

        HL.atualizaView()
        return True
    except Exception as e:
        try:
            D.error(e)
            return False
        finally:
            e = None
            del e


def cancelId(id):
    try:
        B.clear('agendaID' + str(id))
        B.clear('agendaPreID' + str(id))
        B.clear('agendaCnxID' + str(id))
        sitAceitas = [Idioma.traducao('Aguardando'), Idioma.traducao('Agendado')]
        roboCtrl.instance().operContrl.cancelAgendaId(id, Idioma.traducao('Cancelado'), sitAceitas)
        return True
    except Exception as e:
        try:
            D.error(e)
            return False
        finally:
            e = None
            del e