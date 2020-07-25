# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: services\licencajobs.py
# Compiled at: 2019-07-08 19:24:18
import json, requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from models.roboController import *

class oLicenca:

    def __init__(self):
        self.status = -1
        self.idtipo = None
        self.tiponome = None
        self.datainic = None
        self.dataterm = None
        self.dataservidor = None
        self.chave = None
        self.idpacote = None
        self.idafiliado = None


class Licenca:

    def __init__(self):
        self.host = 'http://74.63.254.230:8087/'
        self.service = 'SE1/validalicenca'
        self.Lic = oLicenca()
        self.valida = False
        self.mensagem = ''
        self.resposta = ''

    def get(self, registro):
        self.valida = False
        self.mensagem = ''
        self.resposta = ''
        try:
            dados = {'registro': registro}
            resp = requests.get((self.host + self.service), params=dados, auth=(HTTPBasicAuth('jobs', '123')))
            if resp.status_code != 200:
                self.mensagem = Idioma.traducao('Erro... Não houve comunição com servidor para validar sua licença. Código') + ' ' + str(resp.status_code)
            else:
                data = resp.json()
                ret = False
                msg = ''
                for key, value in data[0].items():
                    if key.upper() == 'STATUS':
                        self.Lic.status = int(value)
                    else:
                        if key.upper() == 'IDTIPO':
                            self.Lic.idtipo = int(value)
                        else:
                            if key.upper() == 'TIPO':
                                self.Lic.tiponome = value
                            else:
                                if key.upper() == 'IDPACOTE':
                                    self.Lic.idpacote = value
                                else:
                                    if key.upper() == 'IDAFILIADO':
                                        self.Lic.idafiliado = value
                                    else:
                                        if key.upper() == 'DATAINIC':
                                            self.Lic.datainic = datetime.strptime(value, '%d/%m/%Y')
                                        else:
                                            if key.upper() == 'DATATERM':
                                                self.Lic.dataterm = datetime.strptime(value, '%d/%m/%Y')
                                            else:
                                                if key.upper() == 'DATAAGORA':
                                                    self.Lic.dataservidor = datetime.strptime(value, '%d/%m/%Y')
                                                else:
                                                    if key.upper() == 'CHAVE':
                                                        self.Lic.chave = value
                    if key.upper() == 'MSG':
                        self.mensagem = value

                if self.Lic.status > 0:
                    if self.Lic.dataterm < self.Lic.dataservidor:
                        self.Lic.status = 0
                        self.mensagem = Idioma.traducao('Licença expirou dia {}').format(self.Lic.dataterm.strftime('%d/%m/%Y'))
                    else:
                        self.valida = True
                        self.resposta = Idioma.traducao('Licença: {} até {}').format(self.Lic.datainic.strftime('%d/%m/%Y'), self.Lic.dataterm.strftime('%d/%m/%Y'))
                        if self.Lic.dataterm - timedelta(days=5) <= self.Lic.dataservidor:
                            self.mensagem = Idioma.traducao('Sua licença vai expirar dia {}\nNão esqueça de renová-la!').format(self.Lic.dataterm.strftime('%d/%m/%Y'))
                else:
                    self.Lic.status = 0
                    self.mensagem = Idioma.traducao('Licença não existe ou está vencida.')
        except:
            self.mensagem = Idioma.traducao('Erro... Não houve comunição com servidor.')