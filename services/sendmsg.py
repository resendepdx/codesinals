# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: services\sendmsg.py
# Compiled at: 2019-07-08 19:24:18
import requests, PySimpleGUI as sg
from loguru import logger as log
import models.roboController as roboCtrl
from models.roboController import *

def atualizaView():
    try:
        roboCtrl.instance().operContrl.wins = 0
        roboCtrl.instance().operContrl.hits = 0
        data = []
        for sinal in roboCtrl.instance().operContrl.agenda:
            item = [
             '{:03d}'.format(int(sinal.op_id)),
             sinal.programmedHour.strftime('%d/%m/%y'),
             sinal.programmedHour.strftime('%H:%M:%S'),
             sinal.pair,
             sinal.direction.upper(),
             sinal.expirationMode,
             sinal.situacao,
             '{:18.2f}'.format(float(sinal.lucro))]
            data.append(item)
            if float(sinal.lucro) > 0:
                roboCtrl.instance().operContrl.wins += 1
            else:
                if float(sinal.lucro) < 0:
                    roboCtrl.instance().operContrl.hits += 1
                elif 'win' in str(sinal.situacao).lower():
                    roboCtrl.instance().operContrl.wins += 1
            if 'loss' in str(sinal.situacao).lower():
                roboCtrl.instance().operContrl.hits += 1

        try:
            roboCtrl.instance().view.janela['-TABLE-'].update(values=data)
            roboCtrl.instance().view.janela.Refresh()
        except Exception as e:
            try:
                log.error(e)
            finally:
                e = None
                del e

        roboCtrl.instance().view.janela['placarW'].update(value=(roboCtrl.instance().operContrl.wins))
        roboCtrl.instance().view.janela['placarH'].update(value=(roboCtrl.instance().operContrl.hits))
        roboCtrl.instance().view.janela['assertividade'].update(value=(roboCtrl.instance().operContrl.getAssertividade()))
        roboCtrl.instance().view.janela['saldolucro'].update(value=(round(roboCtrl.instance().operContrl.saldo, 2)))
    except Exception as e:
        try:
            pass
        finally:
            e = None
            del e