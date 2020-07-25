# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: models\Operation.py
# Compiled at: 2019-07-08 19:24:18
from models.roboController import *

class A:

    def __init__(self, op_id, pair, expirationMode, direction, money, gale1, gale2, hourOrig, programmedHour, expirationDate, expirationGale1, expirationGale2, day, pre_order, typepair='D'):
        self.op_id = op_id
        self.pair = pair
        self.expirationMode = expirationMode
        self.direction = direction
        self.money = money
        self.hourOrig = hourOrig
        self.programmedHour = programmedHour
        self.expirationDate = expirationDate
        self.expirationGale1 = expirationGale1
        self.expirationGale2 = expirationGale2
        self.day = day
        self.gale1 = gale1
        self.gale2 = gale2
        self.pre_order = pre_order
        self.typepair = typepair
        self.payout = 0
        self.trend = ''
        self.situacao = Idioma.traducao('Agendado')
        self.lucro = 0
        self.idIQent = 0
        self.idIQgale1 = 0
        self.idIQgale2 = 0