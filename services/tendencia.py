# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: services\tendencia.py
# Compiled at: 2019-07-08 19:24:18
import time
from datetime import datetime, date, timedelta
from loguru import logger as B
import connection.APIConnection as A

def tendenciaCandles(ativo, expiracao, ticks: int):
    try:
        if ticks <= 0:
            ticks = 2
        doji = 0
        call = 0
        put = 0
        tot = 0
        dire = ''
        seq = ''
        agora = datetime.now() - timedelta(minutes=expiracao)
        hora = datetime.timestamp(agora)
        candles = A.instance().connection.get_candles(ativo, 60 * expiracao, int(ticks), hora)
        for candle in candles:
            tot += 1
            if candle['close'] > candle['open']:
                call += 1
                seq = seq + 'G'
            else:
                if candle['close'] < candle['open']:
                    put += 1
                    seq = seq + 'R'
                else:
                    doji += 1
                    seq = seq + 'C'

        pcall = 0
        pput = 0
        if call > 0:
            pcall = int(round(call / tot) * 100)
        if put > 0:
            pput = int(round(put / tot) * 100)
        if pcall >= 55:
            dire = 'call'
        elif pput >= 55:
            dire = 'put'
    except Exception as inst:
        try:
            B.error(inst)
        finally:
            inst = None
            del inst

    return (
     dire, seq)


def getIndicadores(ativo: str, duracao: int):
    oscila_put = 0
    oscila_neu = 0
    oscila_call = 0
    medias_put = 0
    medias_neu = 0
    medias_call = 0
    pivots_put = 0
    pivots_neu = 0
    pivots_call = 0
    descr_ema = ''
    descr_sma = ''
    tendencia = ''
    descricao = ''
    try:
        data = A.instance().connection.get_technical_indicators(ativo)
        for item in data:
            if int(item['candle_size']) == duracao * 60:
                if not str(item['group']).lower() == 'OSCILLATORS'.lower() or str(item['name']).lower() == 'Relative Strength Index (14)'.lower() or str(item['name']).lower() == 'Stochastic RSI Fast (3, 3, 14, 14)'.lower():
                    if str(item['action']).lower() == 'sell':
                        oscila_put += 1
                    if str(item['action']).lower() == 'buy':
                        oscila_call += 1
                    if str(item['action']).lower() == 'hold':
                        oscila_neu += 1
                if str(item['group']).lower() == 'MOVING AVERAGES'.lower():
                    if str(item['name']).lower() == 'Exponential Moving Average (5)'.lower():
                        if str(item['action']).lower() == 'sell':
                            descr_ema = 'EMA5: VENDER'
                            medias_put += 1
                        if str(item['action']).lower() == 'buy':
                            descr_ema = 'EMA5: COMPRAR'
                            medias_call += 1
                        if str(item['action']).lower() == 'hold':
                            descr_ema = 'EMA5: NEUTRO'
                            medias_neu += 1
                    if str(item['name']).lower() == 'Simple Moving Average (20)'.lower():
                        if str(item['action']).lower() == 'sell':
                            descr_sma = 'SMA20: VENDER'
                            medias_put += 1
                        if str(item['action']).lower() == 'buy':
                            descr_sma = 'SMA20: COMPRAR'
                            medias_call += 1
                        if str(item['action']).lower() == 'hold':
                            descr_sma = 'SMA20: NEUTRO'
                            medias_neu += 1
                if str(item['group']).lower() == 'PIVOTS'.lower():
                    if str(item['action']).lower() == 'sell':
                        pivots_put += 1
                    elif str(item['action']).lower() == 'buy':
                        pivots_call += 1
                    if str(item['action']).lower() == 'hold':
                        pivots_neu += 1

        descricao = descr_ema + ' | ' + descr_sma
        if medias_call > medias_put:
            tendencia = 'call'
        elif medias_put > medias_call:
            tendencia = 'put'
    except:
        pass

    return (
     tendencia, descricao)


def getIndicadores_old(ativo: str, duracao: int):
    oscila_put = 0
    oscila_neu = 0
    oscila_call = 0
    medias_put = 0
    medias_neu = 0
    medias_call = 0
    pivots_put = 0
    pivots_neu = 0
    pivots_call = 0
    try:
        data = A.instance().connection.get_technical_indicators(ativo)
        for item in data:
            if int(item['candle_size']) == duracao * 60:
                if str(item['group']).lower() == 'OSCILLATORS'.lower():
                    if str(item['name']).lower() == 'Relative Strength Index (14)'.lower() or str(item['name']).lower() == 'Stochastic RSI Fast (3, 3, 14, 14)'.lower():
                        if str(item['action']).lower() == 'sell':
                            oscila_put += 1
                        if str(item['action']).lower() == 'buy':
                            oscila_call += 1
                        if str(item['action']).lower() == 'hold':
                            oscila_neu += 1
                if not str(item['group']).lower() == 'MOVING AVERAGES'.lower() or str(item['name']).lower() == 'Exponential Moving Average (5)'.lower() or str(item['name']).lower() == 'Simple Moving Average (20)'.lower():
                    if str(item['action']).lower() == 'sell':
                        medias_put += 1
                    if str(item['action']).lower() == 'buy':
                        medias_call += 1
                    if str(item['action']).lower() == 'hold':
                        medias_neu += 1
                if str(item['group']).lower() == 'PIVOTS'.lower():
                    if str(item['action']).lower() == 'sell':
                        pivots_put += 1
                    elif str(item['action']).lower() == 'buy':
                        pivots_call += 1
                    if str(item['action']).lower() == 'hold':
                        pivots_neu += 1

    except:
        pass

    descricao = 'Médias: CALL={0} PUT={1} NEUTRO={2}'.format(medias_call, medias_put, medias_neu)
    descricao = descricao + '\nOsciladores: CALL={0} PUT={1} NEUTRO={2}'.format(oscila_call, oscila_put, oscila_neu)
    if medias_call + oscila_call > medias_put + medias_neu + oscila_put + oscila_neu:
        tendencia = 'call'
    elif medias_put + oscila_put > medias_call + medias_neu + oscila_call + oscila_neu:
        tendencia = 'put'
    return (tendencia, descricao)