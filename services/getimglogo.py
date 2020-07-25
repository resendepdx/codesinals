# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: services\getimglogo.py
# Compiled at: 2019-07-08 19:24:18
import json, requests, base64
from requests.auth import HTTPBasicAuth

class LogoImg:

    def __init__(self, nomearq='logo.png'):
        self.host = 'http://74.63.254.230:8087/'
        self.service = 'SE1/loadimgjobsplay'
        self.imagembase64 = ''
        self.imagem = nomearq
        self.get()

    def get(self):
        try:
            resp = requests.get((self.host + self.service), auth=(HTTPBasicAuth('jobs', '123')))
            if resp.status_code == 200:
                data = resp.json()
                self.imagembase64 = data['Imagem']
        except:
            pass