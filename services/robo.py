# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: services\robo.py
# Compiled at: 2019-07-08 19:24:18
import time, base64 as M, json, sys as B, os, configparser, PySimpleGUI as sg
from pathlib import Path
from loguru import logger as A
import log.path as R
from log.logger import *
import models.Balance as C
import models.sorosgale as sorosgale
from models.roboController import *
from services import loadlist
from services.ativosopen import AtivosAbertos
import services.scheduleservice as H
from services.licencajobs import Licenca
import connection.APIConnection as API
import connection.RetryConnection as O
from connection.RetryConnection import *
import connection.CreateAPIConnection as N

class Robo:

    def __init__(self, versaoapp):
        self.pathexe = os.getcwd()
        self.arqConfig = 'Config.ini'
        self.arqLista = 'lista.txt'
        self.arqInit = ''
        self.versaoapp = versaoapp
        self.View = None
        self.iniciado = False
        self.avisarLicenca = True
        self.pesqAtviso = AtivosAbertos()
        self.ativosabertos = None
        self.defaultConfig()
        LogConfig()
        self.PararTudo()

    def defaultConfig(self):
        self.email = ''
        self.contareal = False
        self.usarsoros = False
        self.prestop = True
        self.esperarIQ = False
        self.naonoticia = True
        self.notminantes = 0
        self.notminapos = 0
        self.ent_tipo = 'P'
        self.priorid = 0
        self.delay = 0
        self.ent_valor1 = 0
        self.ent_gale1 = 0
        self.ent_gale2 = 0
        self.qtdgales = 1
        self.valorinicial = 0
        self.percent = 0
        self.payoutmin = 80
        self.modelo = 'C'
        self.tipostop = 'P'
        self.stopgain = 1
        self.stoploss = 1
        self.tendusar = False
        self.tendemasma = False
        self.tendvelas = 20
        self.percwinpos = 0
        self.ultrapassoustopwin = False
        self.manterConta = True

    def loadConfig(self):
        if not os.path.isfile(self.arqConfig):
            print(Idioma.traducao('Arquivo não localizado na pasta.'), self.arqConfig)
            self.saveConfig()
            return []
        config = configparser.RawConfigParser()
        config.read(self.arqConfig)
        return config

    def setConfig(self, config):
        try:
            self.email = config['login']['email']
            self.contareal = config['login'].getboolean('contareal', False)
        except:
            self.email = ''
            self.contareal = False

        try:
            self.usarsoros = config['config'].getboolean('soros', False)
            self.prestop = config['config'].getboolean('prestop', False)
            self.esperarIQ = config['config'].getboolean('esperarIQ', False)
            self.delay = int(config['config'].getfloat('delay', 0))
            self.naonoticia = config['config'].getboolean('naonoticia', False)
            self.notminantes = int(config['config'].getfloat('notminantes', 10))
            self.notminapos = int(config['config'].getfloat('notminapos', 30))
            self.priorid = int(config['config'].getfloat('priorid', 0))
        except:
            self.usarsoros = False
            self.prestop = True
            self.esperarIQ = False
            self.delay = 0
            self.naonoticia = True
            self.notminantes = 0
            self.notminapos = 0
            self.priorid = 0

        try:
            self.valorinicial = config['inicio'].getfloat('valorinicial', 0.0)
            self.payoutmin = int(config['inicio'].getfloat('payoutmin', 80))
            self.qtdgales = int(config['inicio'].getfloat('qtdgales', 0))
            if config['inicio'].getboolean('tipostop', True):
                self.tipostop = 'P'
            else:
                self.tipostop = 'V'
            self.stopgain = config['inicio'].getfloat('stopgain', 1.0)
            self.stoploss = config['inicio'].getfloat('stoploss', 1.0)
            self.percwinpos = 0
        except:
            self.valorinicial = 0
            self.payoutmin = 80
            self.qtdgales = 1
            self.tipostop = 'P'
            self.stopgain = 1
            self.stoploss = 1
            self.percwinpos = 0

        try:
            if config['entradafixa'].getboolean('percentual', True):
                self.ent_tipo = 'P'
            else:
                self.ent_tipo = 'V'
            self.ent_valor1 = config['entradafixa'].getfloat('valor1')
            self.ent_gale1 = config['entradafixa'].getfloat('gale1')
            self.ent_gale2 = config['entradafixa'].getfloat('gale2')
        except:
            self.ent_tipo = 'P'
            self.ent_valor1 = 0
            self.ent_gale1 = 0
            self.ent_gale2 = 0

        try:
            self.percent = config['soros'].getfloat('percent')
            if config['soros'].getint('modelo') == 0:
                self.modelo = 'A'
            elif config['soros'].getint('modelo') == 1:
                self.modelo = 'M'
            else:
                self.modelo = 'C'
        except:
            self.percent = 0
            self.modelo = 'C'

        try:
            self.tendusar = config['tendencia'].getboolean('tendusar', False)
            self.tendvelas = int(config['tendencia'].getfloat('tendvelas', 0))
            self.tendemasma = False
        except:
            self.tendusar = False
            self.tendemasma = False
            self.tendvelas = 20

    def saveConfig(self):
        conf = configparser.RawConfigParser()
        conf.read(self.arqConfig)
        secao = 'config'
        if not conf.has_section(secao):
            conf.add_section(secao)
        conf.set(secao, 'soros', str(self.usarsoros))
        conf.set(secao, 'prestop', str(self.prestop))
        conf.set(secao, 'esperarIQ', str(self.esperarIQ))
        conf.set(secao, 'naonoticia', str(self.naonoticia))
        conf.set(secao, 'notminantes', str(self.notminantes))
        conf.set(secao, 'notminapos', str(self.notminapos))
        conf.set(secao, 'delay', str(self.delay))
        conf.set(secao, 'priorid', str(self.priorid))
        secao = 'inicio'
        if not conf.has_section(secao):
            conf.add_section(secao)
        conf.set(secao, 'valorinicial', str(self.valorinicial))
        conf.set(secao, 'payoutmin', str(self.payoutmin))
        conf.set(secao, 'qtdgales', str(self.qtdgales))
        if self.tipostop == 'P':
            conf.set(secao, 'tipostop', str(True))
        else:
            conf.set(secao, 'tipostop', str(False))
        conf.set(secao, 'stopgain', str(self.stopgain))
        conf.set(secao, 'stoploss', str(self.stoploss))
        secao = 'entradafixa'
        if not conf.has_section(secao):
            conf.add_section(secao)
        if self.ent_tipo == 'P':
            conf.set(secao, 'percentual', str(True))
        else:
            conf.set(secao, 'percentual', str(False))
        conf.set(secao, 'valor1', str(self.ent_valor1))
        conf.set(secao, 'gale1', str(self.ent_gale1))
        conf.set(secao, 'gale2', str(self.ent_gale2))
        secao = 'soros'
        if not conf.has_section(secao):
            conf.add_section(secao)
        conf.set(secao, 'percent', str(self.percent))
        if self.modelo == 'A':
            conf.set(secao, 'modelo', '0')
        elif self.modelo == 'M':
            conf.set(secao, 'modelo', '1')
        else:
            conf.set(secao, 'modelo', '2')
        secao = 'tendencia'
        if not conf.has_section(secao):
            conf.add_section(secao)
        conf.set(secao, 'tendusar', str(self.tendusar))
        conf.set(secao, 'tendvelas', str(self.tendvelas))
        conf.set(secao, 'tendemasma', str(self.tendemasma))
        conf.write(open(self.arqConfig, 'w'))

    def saveConfigTP(self, email, contareal):
        conf = configparser.RawConfigParser()
        conf.read(self.arqConfig)
        secao = 'login'
        if not conf.has_section(secao):
            conf.add_section(secao)
        conf.set(secao, 'email', email)
        conf.set(secao, 'contareal', str(contareal))
        conf.write(open(self.arqConfig, 'w'))

    def loadLista(self):
        if not os.path.isfile(self.arqLista):
            print(Idioma.traducao('Arquivo não localizado na pasta.'), self.arqLista)
            self.lista = []
            return 0
        self.lista = []
        qtdlista, self.lista = loadlist.geralista(self.arqLista, self.ent_valor1, self.ent_gale1, self.ent_gale2)
        return qtdlista

    def execAgenda(self):
        self.pesqAtviso.start_ativos()
        while self.iniciado:
            H.B.run_pending()
            time.sleep(1)

    def VerInicio(self):
        pass

    def PararTudo(self):
        self.iniciado = False
        self.pesqAtviso.stop_ativos()
        H.B.clear()

    def VerificarLicenca(self):
        ValidaLicenca = Licenca()
        ValidaLicenca.get(roboCtrl.instance().robo.email)
        roboCtrl.instance().view.janela['-licenca-'].update(value=(ValidaLicenca.resposta))
        roboCtrl.instance().view.janela.Refresh()
        valido = True
        if not ValidaLicenca.valida:
            sg.popup_error((Idioma.traducao('Atenção')), (ValidaLicenca.mensagem), no_titlebar=True,
              keep_on_top=True,
              text_color='black',
              background_color='#DFDDDD')
            valido = False
        elif ValidaLicenca.mensagem != '':
            if self.avisarLicenca:
                self.avisarLicenca = False
                sg.popup_ok((Idioma.traducao('Atenção')), (ValidaLicenca.mensagem), no_titlebar=True,
                  keep_on_top=True,
                  text_color='black',
                  background_color='#DFDDDD')
        return valido

    def Conectar(self):
        T = str(M.b64encode(self.email.encode()))
        self.arqInit = str(R.logs_path) + '/' + T + '_init.conf'
        if os.path.exists(self.arqInit):
            os.remove(self.arqInit)
        if self.contareal:
            self.tipoconta = 'REAL'
        else:
            self.tipoconta = 'PRACTICE'
        if self.ent_tipo == 'P':
            self.ent_valor1 = round(self.valorinicial * self.ent_valor1 / 100, 2)
            self.ent_gale1 = round(self.valorinicial * self.ent_gale1 / 100, 2)
            self.ent_gale2 = round(self.valorinicial * self.ent_gale2 / 100, 2)
        if self.usarsoros:
            self.ent_valor1 = round(self.valorinicial * self.percent / 100, 2)
            self.ent_gale1 = 0
            self.ent_gale2 = 0
            if self.qtdgales > 0:
                self.ent_gale1 = 2
            if self.qtdgales > 1:
                self.ent_gale2 = 2
        else:
            if self.qtdgales < 1:
                self.ent_gale1 = 0
            if self.qtdgales < 2:
                self.ent_gale2 = 0
        if self.loadLista() == 0:
            A.info(Idioma.traducao('Lista vazia ou com dia/horário expirados.'))
        A.info(Idioma.traducao('Aguarde, conectando a IQ...'))
        print(Idioma.traducao('Aguarde, conectando a IQ...'))
        self.View.janela.Refresh()
        N.createapiconnection(self.email, self.senha, self.tipoconta)
        conect = API.instance().connection
        if conect:
            if self.VerificarLicenca():
                C.instance().actual_balance = 0
                if self.tipostop == 'P':
                    X = self.stopgain / 100
                    Z = self.stoploss / 100
                    C.instance().win_limit = self.valorinicial * X
                    C.instance().stop_limit = self.valorinicial * Z * -1
                else:
                    C.instance().win_limit = self.stopgain
                    C.instance().stop_limit = self.stoploss * -1
                A.info('Versão: ' + self.versaoapp)
                A.success(Idioma.traducao('Tipo de conta:') + ' {}', self.tipoconta)
                A.info(Idioma.traducao('Parâmetros iniciais:'))
                A.success(Idioma.traducao('Valor inicial: $') + '{}', round(self.valorinicial, 2))
                A.success(Idioma.traducao('Quantidade de gales:') + ' {}', self.qtdgales)
                A.success(Idioma.traducao('Payout mínimo:') + ' {}', self.payoutmin)
                if self.prestop:
                    A.success(Idioma.traducao('Pré-Stop Loss: Ligado'))
                if self.esperarIQ:
                    A.success(Idioma.traducao('Resultado Resp. IQ'))
                else:
                    A.success(Idioma.traducao('Resultado por Taxas'))
                A.success('Delay: {}', self.delay)
                if self.priorid == 0:
                    A.success(Idioma.traducao('Prioridade') + ': ' + Idioma.traducao('Maior Payout'))
                elif self.priorid == 1:
                    A.success(Idioma.traducao('Prioridade') + ': ' + Idioma.traducao('Digital'))
                elif self.priorid == 2:
                    A.success(Idioma.traducao('Prioridade') + ': ' + Idioma.traducao('Binárias'))
                if self.naonoticia:
                    A.success(Idioma.traducao('Não operar em notícia'))
                if self.tendusar:
                    if self.tendemasma:
                        A.success(Idioma.traducao('Não Operar Contra') + ': ' + Idioma.traducao('Usar EMA5 + SMA20'))
                    else:
                        A.success(Idioma.traducao('Não Operar Contra') + ': ' + Idioma.traducao('Quant. Velas') + ': ' + str(self.tendvelas))
                if not self.usarsoros:
                    A.info(Idioma.traducao('Entradas fixas:'))
                    A.success(Idioma.traducao('Entrada: $') + '{}', round(self.ent_valor1, 2))
                    if self.ent_gale1 > 0:
                        A.success(Idioma.traducao('Gale 1: $') + '{}', round(self.ent_gale1, 2))
                    if self.ent_gale2 > 0:
                        A.success(Idioma.traducao('Gale 2: $') + '{}', round(self.ent_gale2, 2))
                else:
                    A.info('Soros:')
                    if self.modelo == 'A':
                        A.success(Idioma.traducao('Modelo: Agressivo'))
                    elif self.modelo == 'M':
                        A.success(Idioma.traducao('Modelo: Moderado'))
                    else:
                        A.success(Idioma.traducao('Modelo: Conservador'))
                    A.success(Idioma.traducao('1ª entrada: %') + '{} | ' + Idioma.traducao('Valor: $') + '{}', self.percent, round(self.ent_valor1, 2))
                A.warning('WIN %{} - ' + Idioma.traducao('Parar de operar quando atingir: $') + '{}', self.stopgain, round(C.instance().win_limit, 2))
                A.warning('LOSS %{} - ' + Idioma.traducao('Parar de operar quando atingir: $') + '{}', self.stoploss, round(C.instance().stop_limit, 2))
                print('Versão: ' + self.versaoapp)
                print(Idioma.traducao('Tipo de conta:'), self.tipoconta)
                print(Idioma.traducao('Parâmetros iniciais:'))
                print(Idioma.traducao('Quantidade de gales:'), self.qtdgales)
                print(Idioma.traducao('Payout mínimo:'), self.payoutmin)
                if self.prestop:
                    print(Idioma.traducao('Pré-Stop Loss: Ligado'))
                if self.esperarIQ:
                    print(Idioma.traducao('Resultado Resp. IQ'))
                else:
                    print(Idioma.traducao('Resultado por Taxas'))
                print('Delay: ', self.delay)
                if self.priorid == 0:
                    print(Idioma.traducao('Prioridade') + ': ' + Idioma.traducao('Maior Payout'))
                elif self.priorid == 1:
                    print(Idioma.traducao('Prioridade') + ': ' + Idioma.traducao('Digital'))
                elif self.priorid == 2:
                    print(Idioma.traducao('Prioridade') + ': ' + Idioma.traducao('Binárias'))
                if self.naonoticia:
                    print(Idioma.traducao('Não operar em notícia'))
                if self.tendusar:
                    if self.tendemasma:
                        print(Idioma.traducao('Não Operar Contra') + ': ' + Idioma.traducao('Usar EMA5 + SMA20'))
                    else:
                        print(Idioma.traducao('Não Operar Contra') + ': ' + Idioma.traducao('Quant. Velas') + ': ' + str(self.tendvelas))
                if not self.usarsoros:
                    print(Idioma.traducao('Entradas fixas:'))
                    print(Idioma.traducao('Entrada: $'), round(self.ent_valor1, 2))
                    if self.ent_gale1 > 0:
                        print(Idioma.traducao('Gale 1: $'), round(self.ent_gale1, 2))
                    if self.ent_gale2 > 0:
                        print(Idioma.traducao('Gale 2: $'), round(self.ent_gale2, 2))
                else:
                    print('Soros:')
                    if self.modelo == 'A':
                        print(Idioma.traducao('Modelo: Agressivo'))
                    elif self.modelo == 'M':
                        print(Idioma.traducao('Modelo: Moderado'))
                    else:
                        print(Idioma.traducao('Modelo: Conservador'))
                    print((Idioma.traducao('1ª entrada: %') + '{0} | ' + Idioma.traducao('Valor: $') + '{1}').format(self.percent, round(self.ent_valor1, 2)))
                self.View.janela['valorinic'].update(value=(round(self.valorinicial, 2)))
                self.View.janela['saldoatual'].update(value=(C.instance().balance))
                self.View.janela['stopgainp'].update(value=(self.stopgain))
                self.View.janela['stopgainv'].update(value=(round(C.instance().win_limit, 2)))
                self.View.janela['stoplossp'].update(value=(self.stoploss))
                self.View.janela['stoplossv'].update(value=(round(C.instance().stop_limit, 2)))
                self.View.janela.Refresh()
                if not self.usarsoros:
                    self.valorinicial = 0
                C.instance().sorosgale.config_ini(self.valorinicial, self.percent, self.modelo)
                return True
        return False

    def IniciarAgendamentos(self):
        H.C(self.lista)
        A.info(Idioma.traducao('Agendamento realizado com sucesso!'))
        print(Idioma.traducao('Agendamento realizado com sucesso!'))
        self.iniciado = True

    def ExecutaAgendamento(self):
        self.VerInicio()
        try:
            O().verify_connection()
            self.execAgenda()
        except Exception as e:
            try:
                A.error(e)
            finally:
                e = None
                del e