# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: models\sorosgale.py
# Compiled at: 2019-07-08 19:24:18


class sorosgale:

    def __init__(self):
        self.payout = 80
        self.modelo = 'A'
        self.perc_entrada = 1
        self.valor_lucro = 0
        self.count_soros = 0
        self.count_win = 0
        self.count_loss = 0
        self.valor_entrada = 0
        self.valor_recuperar = 0
        self.qtdgales = 0
        self.entrada_inicial = self.valor_entrada

    def config_ini(self, valor_inicial: float, perc_entrada: float, modelo: str='C'):
        self.modelo = modelo.upper()
        self.perc_entrada = perc_entrada
        self.valor_inicial = valor_inicial
        self.valor_lucro = 0
        self.total_soros = 0
        self.fator_soros = 0
        if self.modelo == 'A':
            self.total_soros = 1
            self.fator_soros = 0.5
        elif self.modelo == 'M':
            self.total_soros = 1
            self.fator_soros = 0.4
        elif self.modelo == 'C':
            self.total_soros = 1
        self.fator_valor = round(self.valor_inicial * self.fator_soros / 100, 2)
        self.count_soros = 0
        self.count_win = 0
        self.count_loss = 0
        self.valor_recuperar = 0
        self.valor_entrada = 0
        self.calculo_entrada_inicial(self.valor_inicial)
        self.entrada_inicial = self.valor_entrada

    def calculo_entrada_inicial(self, valor: float):
        self.valor_entrada = round(valor * self.perc_entrada / 100, 2)
        self.valor_lucro = round(self.valor_entrada * self.payout / 100, 2)

    def calculo_entrada_loss(self, valor: float):
        self.valor_entrada = round(self.valor_recuperar / self.payout * 100, 2)
        if self.fator_soros > 0:
            self.valor_entrada = round(self.valor_entrada + self.fator_valor * (self.payout / 100), 2)
        self.valor_lucro = round(self.valor_entrada * self.payout / 100, 2)

    def calcValorEntrada(self, payout: float):
        if payout == 0:
            self.payout = 80
        else:
            self.payout = payout
        if self.count_win == 0 and self.count_loss == 0:
            self.calculo_entrada_inicial(self.valor_inicial)
        elif self.valor_lucro > 0:
            if self.count_soros <= self.total_soros and self.valor_entrada == self.entrada_inicial:
                self.valor_entrada = self.valor_entrada + self.valor_lucro
                self.valor_lucro = round(self.valor_entrada * self.payout / 100, 2)
            else:
                self.count_soros = 0
                self.valor_entrada = self.entrada_inicial
                self.valor_lucro = round(self.valor_entrada * self.payout / 100, 2)
            self.count_soros += 1
        elif self.valor_lucro < 0:
            self.count_soros = 0
            self.calculo_entrada_loss(self.valor_recuperar)

    def execute(self, result: float=0):
        self.valor_lucro = round(result, 2)
        if self.valor_lucro > 0:
            self.count_win += 1
            if self.valor_recuperar > 0:
                self.valor_recuperar = round(self.valor_recuperar - self.valor_lucro, 2)
            if self.valor_recuperar < 0:
                self.valor_recuperar = 0
        elif self.valor_lucro < 0:
            self.count_loss += 1
            self.valor_recuperar = round(self.valor_recuperar + self.valor_entrada, 2)