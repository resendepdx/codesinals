# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: personal\dencryptfile.py
# Compiled at: 2019-07-08 19:24:18
import glob, os, json, cryptography
from cryptography.fernet import Fernet
KEY_TEMPLATES = 'Fqw6W1xiDGdsWdTaiEeRyjxRko21-X5FNooGiUI1K-0='

def getTemplate(input_file):
    retjson = None
    fernet = Fernet(KEY_TEMPLATES)
    data = None
    with open(input_file, 'rb') as f:
        data = f.read()
    decrypted = fernet.decrypt(data)
    retjson = json.loads(decrypted)
    return retjson