# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: services\downloadlista.py
# Compiled at: 2019-07-08 19:24:18
import json, requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from models.roboController import *
import base64

class ListaSinais:

    def __init__(self):
        self.host = 'http://74.63.254.230:8087/'
        self.servicelista = 'SE1/jobsplaylista'
        self.servicearq = 'SE1/downloadlista'
        self.lista = []

    def getLista(self, idafiliado):
        self.lista = []
        try:
            dados = {'afiliado': idafiliado}
            resp = requests.get((self.host + self.servicelista), params=dados, auth=(HTTPBasicAuth('jobs', '123')))
            if resp.status_code == 200:
                self.lista = resp.json()
        except:
            pass

    def getArquivo(self, id):
        data = None
        try:
            dados = {'id': id}
            resp = requests.get((self.host + self.servicearq), params=dados, auth=(HTTPBasicAuth('jobs', '123')))
            if resp.status_code == 200:
                data = base64.decodestring(resp.content)
        except:
            pass

        return data