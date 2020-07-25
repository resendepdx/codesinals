# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: services\loadlist.py
# Compiled at: 2019-07-08 19:24:18
import time
from datetime import datetime, timedelta
import simplejson as Y
from collections import OrderedDict as X
import csv
from models.roboController import *
import models.roboController as roboCtrl
V = 'Nao agendado'
U = 'Situação'
T = 'Expiração(Min)'
S = 'Gale 2($)'
R = 'Gale 1($)'
Q = 'Valor($)'
P = 'Operação'
O = 'Dia'
N = 'Ativo'
K = 'ID'
J = 'Horário'
H = ':'

def remove_carespeciais(old):
    to_remove = '!@#$%¨&ï»¿'
    new_string = old
    for x in to_remove:
        new_string = new_string.replace(x, '')

    return new_string


def geralista(arq, ent_valor1, ent_gale1, ent_gale2):
    W = []
    tmp = []
    cnt = 0
    b = None
    try:
        with open(arq) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            cnt = 0
            line_count = 0
            for B in csv_reader:
                if B:
                    if str(B[0]) != 'Moeda':
                        if str(B[0]) != 'Ativo':
                            if str(B[0]) != '':
                                A = X()
                                hr = B[2].split(H)
                                F = '{:02d}'.format(int(hr[0]))
                                G = '{:02d}'.format(int(hr[1]))
                                try:
                                    I = str(hr[2])
                                except:
                                    I = str('00')

                                cnt += 1
                                try:
                                    A[K] = int(cnt)
                                    A[N] = remove_carespeciais(str(B[0]).strip())
                                    A[O] = int(B[1].strip())
                                    A[J] = str(F) + H + str(G) + H + str(I)
                                    A[P] = remove_carespeciais(str(B[3]).strip())
                                    A[Q] = B[4].strip()
                                    A[R] = B[5].strip()
                                    A[S] = B[6].strip()
                                    A[T] = int(B[7])
                                    A[U] = V
                                except:
                                    A[K] = int(cnt)
                                    A[N] = remove_carespeciais(str(B[0]).strip())
                                    A[O] = int(B[1].strip())
                                    A[J] = str(F) + H + str(G) + H + str(I)
                                    A[P] = remove_carespeciais(str(B[3]).strip())
                                    A[Q] = ent_valor1
                                    A[R] = ent_gale1
                                    A[S] = ent_gale2
                                    A[T] = int(B[4].strip())
                                    A[U] = V

                                if roboCtrl.instance().robo.usarsoros:
                                    pesq = str(F) + H + str(G)
                                    if pesq in tmp:
                                        valid = False
                                    else:
                                        tmp.append(pesq)
                                        valid = True
                                else:
                                    valid = True
                                if valid:
                                    W.append(A)
                    line_count += 1

        WS = sorted(W, key=(lambda i: (i[O], i[J])))
        b = Y.dumps(WS)
    except:
        raise Exception(Idioma.traducao('Layout inválido.\nLayout correto: ATIVO;DIA;HORARIO;DIRECAO;DURACAO'))

    return (cnt, b)