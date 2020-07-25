# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: services\buyservice.py
# Compiled at: 2019-07-08 19:24:18
import json, time as D
from loguru import logger as A
from datetime import date
import models.Balance as BL
import models.roboController as roboCtrl
from models.roboController import *
from models.ThreadOperacion import *
import connection.APIConnection as ApiCon
import services.buycontroller as E
import services.scheduleservice as Agenda
import services.sendmsg as HL
from services.noticias import *
from iqoptionapi.expiration import *
S = None
R = ','
Q = '.'
P = float
H = True
K = ''
C = int
G = False
F = str
MsgQueda = 'ID:{} ' + Idioma.traducao('Queda de Internet durante a Operacao')

class O:
    SECOND_RESULT = 2
    VELAPEQUENA = 9

    def atualView(self):
        D.sleep(2)
        HL.atualizaView()

    def atualizarTela(self):
        B = ThreadOper(target=(self.atualView))
        roboCtrl.instance().add_listThread = B
        B.start()

    def dooperation(self, operation):
        B = ThreadOper(target=(self.start_operation), args=(operation,))
        roboCtrl.instance().add_listThread = B
        B.start()

    def docancelProxSinal(self, operation, gale=0):
        B = ThreadOper(target=(self.cancelProxSinal), args=(operation, gale))
        roboCtrl.instance().add_listThread = B
        B.start()

    def doresultIQ(self, operation, id, gale):
        B = ThreadOper(target=(self.resultIQ), args=(operation, id, gale))
        roboCtrl.instance().add_listThread = B
        B.start()

    def tamanhoVela(self, vopen, vclose):
        pequena = False
        try:
            vopenv = str(vopen).split('.')[1]
            vclosev = str(vclose).split('.')[1]
            vclosev = '{:<06d}'.format(int(vclosev))
            vopenv = '{:<06d}'.format(int(vopenv))
            vopenv = int(vopenv)
            vclosev = int(vclosev)
            vdifer = abs(vopenv - vclosev)
            if vdifer < self.VELAPEQUENA:
                pequena = True
        except:
            pequena = False

        return pequena

    def calcValorFatorReducao(self, fator: float, value: float):
        return round(value * (fator / 100), 2)

    def atualizaNovosValoresPosStopWin(self):
        roboCtrl.instance().robo.ultrapassoustopwin = True
        BL.instance().stop_limit = calcValorFatorReducao(1 - roboCtrl.instance().robo.percwinpos, BL.instance().win_limit)
        BL.instance().win_limit = calcValorFatorReducao(roboCtrl.instance().robo.percwinpos, BL.instance().win_limit)
        roboCtrl.instance().robo.ent_valor1 = calcValorFatorReducao(roboCtrl.instance().robo.percwinpos, roboCtrl.instance().robo.ent_valor1)
        roboCtrl.instance().robo.ent_gale1 = calcValorFatorReducao(roboCtrl.instance().robo.percwinpos, roboCtrl.instance().robo.ent_gale1)
        roboCtrl.instance().robo.ent_gale2 = calcValorFatorReducao(roboCtrl.instance().robo.percwinpos, roboCtrl.instance().robo.ent_gale2)
        roboCtrl.instance().view.janela['stopgainv'].update(value=(round(C.instance().win_limit, 2)))
        roboCtrl.instance().view.janela['stoplossv'].update(value=(round(C.instance().stop_limit, 2)))
        if not roboCtrl.instance().robo.usarsoros:
            msg = Idioma.traducao('Entradas fixas:')
            A.info(msg)
            print(msg)
            msg = (Idioma.traducao('Entrada: $') + '{0}').format(round(roboCtrl.instance().robo.ent_valor1, 2))
            A.info(msg)
            print(msg)
            if roboCtrl.instance().robo.ent_gale1 > 0:
                msg = (Idioma.traducao('Gale 1: $') + '{0}').format(round(roboCtrl.instance().robo.ent_gale1, 2))
                A.info(msg)
                print(msg)
            if roboCtrl.instance().robo.ent_gale2 > 0:
                msg = (Idioma.traducao('Gale 2: $') + '{0}').format(round(roboCtrl.instance().robo.ent_gale2, 2))
                A.info(msg)
                print(msg)
        else:
            roboCtrl.instance().sorosgale.config_ini(calcValorFatorReducao(roboCtrl.instance().robo.percwinpos, roboCtrl.instance().robo.valorinicial), roboCtrl.instance().robo.percent, roboCtrl.instance().robo.modelo)

    def mostrar_saldo(self):
        A.warning('Stop Gain: {} | Stop Loss: {} | ' + Idioma.traducao('Lucro atual: $') + '{}', BL.instance().win_limit, BL.instance().stop_limit, round(BL.instance().actual_balance, 2))
        print((Idioma.traducao('Lucro atual: $') + '{0}').format(round(BL.instance().actual_balance, 2)))

    def stop_operation(self, operation, valorProxEntrada: float):
        B = operation
        if BL.instance().actual_balance <= BL.instance().stop_limit:
            msg = ('ID:{0} [STOP LOSS] ' + Idioma.traducao('Lucro atual: $') + '{1}').format(B.op_id, round(BL.instance().actual_balance, 2))
            A.info(msg)
            print(msg)
            Agenda.cancel(B.op_id)
            return True
        if BL.instance().actual_balance - valorProxEntrada <= BL.instance().stop_limit:
            if BL.instance().actual_balance != 0:
                if roboCtrl.instance().robo.prestop:
                    msg = ('ID:{0} [PRE-STOP LOSS] ' + Idioma.traducao('Entrada: $') + '{1} ' + Idioma.traducao('Lucro previsto: $') + '{2}').format(B.op_id, valorProxEntrada, round(BL.instance().actual_balance - valorProxEntrada, 2))
                    A.info(msg)
                    print(msg)
                    Agenda.cancel(B.op_id)
                    return True
        if BL.instance().actual_balance >= BL.instance().win_limit:
            msg = ('ID:{0} [STOP WIN] ' + Idioma.traducao('Lucro atual: $') + '{1}').format(B.op_id, round(BL.instance().actual_balance, 2))
            A.info(msg)
            print(msg)
            if roboCtrl.instance().robo.percwinpos > 0:
                if not roboCtrl.instance().robo.ultrapassoustopwin:
                    self.atualizaNovosValoresPosStopWin()
                    return False
                Agenda.cancel(B.op_id)
                return True
        else:
            return False

    def start_operation(self, operation):
        H = '0'
        B = operation
        dhmax = B.programmedHour + timedelta(seconds=20)
        if C(date.today().day) == C(B.day):
            if datetime.now() >= B.programmedHour:
                if datetime.now() <= dhmax:
                    if int(B.payout) < int(roboCtrl.instance().robo.payoutmin):
                        if int(B.payout) > 0:
                            if int(B.payout) == 0:
                                msg = ('ID:{0} ' + Idioma.traducao('Expiração Indisponível') + ' ' + Idioma.traducao('Payout inferior:') + ' {1} ' + Idioma.traducao('atual:') + ' {2}').format(B.op_id, int(roboCtrl.instance().robo.payoutmin), int(B.payout))
                                A.warning(msg)
                                print(msg)
                                roboCtrl.instance().operContrl.calculoTotal(B.op_id, Idioma.traducao('Expiração Indisponível'))
                            else:
                                msg = ('ID:{0} ' + Idioma.traducao('Payout inferior:') + ' {1} ' + Idioma.traducao('atual:') + ' {2}').format(B.op_id, int(roboCtrl.instance().robo.payoutmin), int(B.payout))
                                A.warning(msg)
                                print(msg)
                                roboCtrl.instance().operContrl.calculoTotal(B.op_id, 'Payout {0}'.format(int(B.payout)))
                            self.atualizarTela()
                            return
                    if BL.instance().moeda == 'BRL':
                        if float(B.money) < 2:
                            msg = ('ID:{0} ' + Idioma.traducao('Entrada: $') + '{1} ' + Idioma.traducao('inválido para a moeda') + ' [{2}] ' + Idioma.traducao('mínimo de $') + '2.00').format(B.op_id, float(B.money), BL.instance().moeda)
                            A.info(msg)
                            print(msg)
                            return
                    if BL.instance().moeda == 'USD':
                        if float(B.money) < 1:
                            msg = ('ID:{0} ' + Idioma.traducao('Entrada: $') + '{1} ' + Idioma.traducao('inválido para a moeda') + ' [{2}] ' + Idioma.traducao('mínimo de $') + '1.00').format(B.op_id, float(B.money), BL.instance().moeda)
                            A.info(msg)
                            print(msg)
                            return
                    if B.direction != B.trend:
                        if B.trend != '':
                            msg = ('ID:{0} {1} {2} ' + Idioma.traducao('Contra Têndencia') + ' {3}').format(B.op_id, B.pair, B.direction, B.trend)
                            A.warning(msg)
                            print(msg)
                            roboCtrl.instance().operContrl.calculoTotal(B.op_id, Idioma.traducao('Contra Têndencia'))
                            self.atualizarTela()
                            return
                    if roboCtrl.instance().robo.naonoticia:
                        tem, noticia = PesquisaNoticia(B.programmedHour.strftime('%H:%M:%S'), B.pair)
                        if tem:
                            msg = ('ID:{0} {1} {2} ' + Idioma.traducao('Existe notícia de 3 touros') + '\n{3} {4} {5}').format(B.op_id, B.pair, B.programmedHour.strftime('%H:%M:%S'), noticia.hora, noticia.moeda, noticia.texto)
                            A.warning(msg)
                            print(msg)
                            roboCtrl.instance().operContrl.calculoTotal(B.op_id, Idioma.traducao('Notícia'))
                            self.atualizarTela()
                            return
                    self.buy(B)
                    D.sleep(1)

    def cancelProxSinal(self, operation, gale=0):
        if roboCtrl.instance().robo.usarsoros:
            time.sleep(2)
            try:
                B = operation
                dhInic = operation.hourOrig
                if gale == 0:
                    dhTerm = operation.expirationDate
                elif gale == 1:
                    dhTerm = operation.expirationGale1
                else:
                    dhTerm = operation.expirationGale2
                for sinal in roboCtrl.instance().operContrl.agenda:
                    if sinal.programmedHour >= dhInic:
                        if sinal.programmedHour <= dhTerm:
                            if sinal.op_id != operation.op_id:
                                if not sinal.situacao == Idioma.traducao('Aguardando'):
                                    if sinal.situacao == Idioma.traducao('Agendado'):
                                        pass
                                Agenda.cancelId(sinal.op_id)
                                msg = 'ID:{0} {1} {2} Cancelado Sobreposto'.format(sinal.op_id, sinal.pair, sinal.programmedHour.strftime('%H:%M:%S'))
                                A.warning(msg)
                                print(msg)

                self.atualizarTela()
            except Exception as e:
                try:
                    A.error(e)
                finally:
                    e = None
                    del e

    def resultIQ(self, operation, id, gale):
        B = operation
        if gale == 1:
            vgale = 'Gale1'
            dhExp = B.expirationGale1
        elif gale == 2:
            vgale = 'Gale2'
            dhExp = B.expirationGale2
        else:
            vgale = ''
            dhExp = B.expirationDate
        check, win = E.D(id, B.typepair, dhExp)
        if check:
            win = round(win, 2)
            BL.instance().actual_balance = BL.instance().actual_balance + win
            if win > 0:
                msg = 'ID:{0} {1} {2} Payout {3} Cod:{4} WIN ${5}'.format(B.op_id, vgale.upper(), B.pair, int(B.payout), id, win)
                A.success(msg)
                msg = 'ID:{0} {1} {2} Payout {3} WIN ${4}'.format(B.op_id, vgale.upper(), B.pair, int(B.payout), win)
                print(msg)
                if gale == 0:
                    roboCtrl.instance().operContrl.calculoTotal(B.op_id, 'Win', win)
                else:
                    roboCtrl.instance().operContrl.calculoTotal(B.op_id, 'Win ' + vgale, 0, win)
            elif win < 0 or B.typepair == 'D':
                msg = 'ID:{0} {1} {2} Payout {3} Cod:{4} LOSS ${5}'.format(B.op_id, vgale.upper(), B.pair, int(B.payout), id, win)
                A.error(msg)
                msg = 'ID:{0} {1} {2} Payout {3} LOSS ${4}'.format(B.op_id, vgale.upper(), B.pair, int(B.payout), win)
                print(msg)
                if gale == 0:
                    roboCtrl.instance().operContrl.calculoTotal(B.op_id, 'Loss', win)
                else:
                    roboCtrl.instance().operContrl.calculoTotal(B.op_id, 'Loss ' + vgale, 0, win)
            else:
                msg = 'ID:{0} {1} {2} Payout {3} Cod:{4} DOJI ${5}'.format(B.op_id, vgale.upper(), B.pair, int(B.payout), id, win)
                A.success(msg)
                msg = 'ID:{0} {1} {2} Payout {3} DOJI ${4}'.format(B.op_id, vgale.upper(), B.pair, int(B.payout), win)
                print(msg)
                roboCtrl.instance().operContrl.calculoTotal(B.op_id, 'Doji')
            self.atualizarTela()
            self.mostrar_saldo()
        return (
         check, win)

    def buy(self, operation):
        B = operation

        def resultado_candle(valorent, taxa):
            try:
                candle = E.getCandles(B.pair, int(B.expirationMode), 1)
                txclose = 0
                velaPeq = False
                if candle:
                    chkres = True
                    if taxa <= 0:
                        taxa = candle[0]['open']
                    txclose = candle[0]['close']
                    if txclose > taxa:
                        cor = 'G'
                    elif txclose < taxa:
                        cor = 'R'
                    else:
                        cor = 'C'
                    lucro = 0
                    if not (cor == 'G' and B.direction == 'call'):
                        if not cor == 'R' or B.direction == 'put':
                            lucro = round(float(valorent) * (int(B.payout) / 100), 2)
                        else:
                            lucro = float(valorent) * -1
                        velaPeq = self.tamanhoVela(taxa, txclose)
                else:
                    chkres = False
                    lucro = 0
            except:
                chkres = False

            return (chkres, float(lucro), txclose, velaPeq)

        valor = B.money
        if roboCtrl.instance().robo.usarsoros:
            BL.instance().sorosgale.calcValorEntrada(B.payout)
        if BL.instance().sorosgale.valor_entrada > 0:
            valor = BL.instance().sorosgale.valor_entrada
        if roboCtrl.instance().robo.percwinpos > 0:
            if roboCtrl.instance().robo.ultrapassoustopwin:
                valor = calcValorFatorReducao(roboCtrl.instance().robo.percwinpos, valor)
        if self.stop_operation(B, float(valor)):
            return
        if B.idIQent > 0:
            A.error('ID:{} Entrada Repetida Cancelada Cod: {}', B.op_id, B.idIQent)
            return
        S, C, tx = E.C(B, valor)
        if S:
            B.idIQent = C
            if B.typepair == 'D':
                tipoent = 'Digital'
            else:
                tipoent = 'Binaria'
            A.debug('ID:{} {} {} {}M Payout {} {} {} ${} Cod: {} criada com sucesso', B.op_id, B.programmedHour, B.pair, B.expirationMode, B.payout, tipoent, B.direction, round(float(valor), 2), C)
            roboCtrl.instance().operContrl.calculoTotal(B.op_id, Idioma.traducao('1ª Entrada'))
            self.atualizarTela()
            self.docancelProxSinal(B)
            if not roboCtrl.instance().robo.esperarIQ:
                check = False
                dhexpira = B.expirationDate - timedelta(seconds=(self.SECOND_RESULT))
                while not check:
                    if datetime.now() >= dhexpira:
                        vchkres, vret, vtxclose, vtamPeq = resultado_candle(float(valor), tx)
                        check = True
                    else:
                        time.sleep(1)

                if not (check and vtamPeq or vchkres):
                    if vtamPeq:
                        A.info('ID:{} {} Tx({} x {}) Vela pequena, aguardar resultado IQ...', B.op_id, B.pair, tx, vtxclose)
                    else:
                        A.info('ID:{} {} Não houve retorno de taxas, aguardar resultado IQ...', B.op_id, B.pair, tx, vtxclose)
                    check, vret = self.resultIQ(B, C, 0)
                else:
                    self.doresultIQ(B, C, 0)
            else:
                check, vret = self.resultIQ(B, C, 0)
                vtamPeq = False
            if check:
                if not roboCtrl.instance().robo.esperarIQ:
                    if not vtamPeq:
                        msg = 'ID:{0} {1} Tx({2} x {3})'.format(B.op_id, B.pair, tx, vtxclose)
                        A.info(msg)
                        print(msg)
                if roboCtrl.instance().robo.usarsoros:
                    BL.instance().sorosgale.execute(vret)
                if not vret < 0:
                    if not vret == 0 or B.typepair == 'D':
                        if roboCtrl.instance().robo.qtdgales > 0:
                            self.buy_gale1(B)
        else:
            if roboCtrl.instance().robo.usarsoros:
                BL.instance().sorosgale.valor_lucro = 0
            msg = 'ID:{0} {1} ${2} - {3} {4}'.format(B.op_id, B.pair, round(float(valor), 2), Idioma.traducao('Resposta IQ:'), C)
            A.error(msg)
            print(msg)
            roboCtrl.instance().operContrl.calculoTotal(B.op_id, Idioma.traducao('Fechado'))
            self.atualizarTela()

    def buy_gale1(self, operation, loopgale: bool=False):
        B = operation

        def resultado_candle(valorent, taxa):
            try:
                candle = E.getCandles(B.pair, int(B.expirationMode), 1)
                txclose = 0
                velaPeq = False
                if candle:
                    chkres = True
                    if taxa <= 0:
                        taxa = candle[0]['open']
                    txclose = candle[0]['close']
                    if txclose > taxa:
                        cor = 'G'
                    elif txclose < taxa:
                        cor = 'R'
                    else:
                        cor = 'C'
                    lucro = 0
                    if not (cor == 'G' and B.direction == 'call'):
                        if not cor == 'R' or B.direction == 'put':
                            lucro = round(float(valorent) * (int(B.payout) / 100), 2)
                        else:
                            lucro = float(valorent) * -1
                        velaPeq = self.tamanhoVela(taxa, txclose)
                else:
                    chkres = False
                    lucro = 0
            except:
                chkres = False

            return (chkres, float(lucro), txclose, velaPeq)

        if P(B.gale1.replace(Q, K).replace(R, K)) == 0:
            A.warning('ID:{} GALE1 Desligado {}', B.op_id, B.pair)
            return
        valor = B.gale1
        if loopgale:
            if roboCtrl.instance().robo.usarsoros:
                valor = BL.instance().sorosgale.valor_entrada
        else:
            if roboCtrl.instance().robo.usarsoros:
                BL.instance().sorosgale.calcValorEntrada(B.payout)
            if BL.instance().sorosgale.valor_entrada > 0:
                if roboCtrl.instance().robo.qtdgales < 1:
                    A.warning('ID:{} GALE1 Desligado {}', B.op_id, B.pair)
                    return
                valor = BL.instance().sorosgale.valor_entrada
            if roboCtrl.instance().robo.percwinpos > 0:
                if roboCtrl.instance().robo.ultrapassoustopwin:
                    valor = calcValorFatorReducao(roboCtrl.instance().robo.percwinpos, valor)
        if self.stop_operation(B, float(valor)):
            return
        if B.idIQgale1 > 0:
            A.error('ID:{} GALE1 Entrada Repetida Cancelada Cod: {}', B.op_id, B.idIQgale1)
            return
        S, C, tx = E.C(B, valor)
        if S:
            B.idIQgale1 = C
            if B.typepair == 'D':
                tipoent = 'Digital'
            else:
                tipoent = 'Binaria'
            A.debug('ID:{} GALE1 {} {}M Payout {} {} {} ${} Cod: {} criada com sucesso', B.op_id, B.pair, B.expirationMode, B.payout, tipoent, B.direction, round(float(valor), 2), C)
            roboCtrl.instance().operContrl.calculoTotal(B.op_id, 'Gale 1')
            self.atualizarTela()
            self.docancelProxSinal(B, 1)
            if not roboCtrl.instance().robo.esperarIQ:
                check = False
                dhexpira = B.expirationGale1 - timedelta(seconds=(self.SECOND_RESULT))
                while not check:
                    if datetime.now() >= dhexpira:
                        vchkres1, vret1, vtxclose, vtamPeq = resultado_candle(float(valor), tx)
                        check = True
                    else:
                        time.sleep(1)

                if not (check and vtamPeq or vchkres1):
                    if vtamPeq:
                        A.info('ID:{} GALE1 {} Tx({} x {}) Vela pequena, aguardar resultado IQ...', B.op_id, B.pair, tx, vtxclose)
                    else:
                        A.info('ID:{} GALE1 {} Não houve retorno de taxas, aguardar resultado IQ...', B.op_id, B.pair, tx, vtxclose)
                    check, vret = self.resultIQ(B, C, 1)
                else:
                    self.doresultIQ(B, C, 1)
            else:
                check, vret1 = self.resultIQ(B, C, 1)
                vtamPeq = False
            if check:
                if not roboCtrl.instance().robo.esperarIQ:
                    if not vtamPeq:
                        msg = 'ID:{0} GALE1 {1} Tx({2} x {3})'.format(B.op_id, B.pair, tx, vtxclose)
                        A.info(msg)
                        print(msg)
                if roboCtrl.instance().robo.usarsoros:
                    BL.instance().sorosgale.execute(vret1)
                if vret1 < 0:
                    self.buy_gale2(B)
                elif not vret1 == 0 or B.typepair != 'D':
                    self.buy_gale1(B)
        else:
            if roboCtrl.instance().robo.usarsoros:
                BL.instance().sorosgale.valor_lucro = 0
            msg = 'ID:{0} GALE1 {1} ${2} - {3} {4}'.format(B.op_id, B.pair, round(float(valor), 2), Idioma.traducao('Resposta IQ:'), C)
            A.error(msg)
            print(msg)

    def buy_gale2(self, operation, loopgale: bool=False):
        B = operation
        if P(B.gale2.replace(Q, K).replace(R, K)) == 0:
            A.warning('ID:{} GALE2 Desligado {}', B.op_id, B.pair)
            return
        valor = B.gale2
        if loopgale:
            if roboCtrl.instance().robo.usarsoros:
                valor = BL.instance().sorosgale.valor_entrada
        else:
            if roboCtrl.instance().robo.usarsoros:
                BL.instance().sorosgale.calcValorEntrada(B.payout)
            if BL.instance().sorosgale.valor_entrada > 0:
                if roboCtrl.instance().robo.qtdgales < 2:
                    A.warning('ID:{} GALE2 Desligado {}', B.op_id, B.pair)
                    return
                valor = BL.instance().sorosgale.valor_entrada
            if roboCtrl.instance().robo.percwinpos > 0:
                if roboCtrl.instance().robo.ultrapassoustopwin:
                    valor = calcValorFatorReducao(roboCtrl.instance().robo.percwinpos, valor)
        if self.stop_operation(B, float(valor)):
            return
        if B.idIQgale2 > 0:
            A.error('ID:{} GALE2 Entrada Repetida Cancelada Cod: {}', B.op_id, B.idIQgale1)
            return
        S, C, tx = E.C(B, valor)
        if S:
            B.idIQgale2 = C
            if B.typepair == 'D':
                tipoent = 'Digital'
            else:
                tipoent = 'Binaria'
            A.debug('ID:{} GALE2 {} {}M Payout {} {} {} ${} Cod: {} criada com sucesso', B.op_id, B.pair, B.expirationMode, B.payout, tipoent, B.direction, round(float(valor), 2), C)
            roboCtrl.instance().operContrl.calculoTotal(B.op_id, 'Gale 2')
            self.atualizarTela()
            self.docancelProxSinal(B, 2)
            check, vret2 = self.resultIQ(B, C, 2)
            if check:
                if roboCtrl.instance().robo.usarsoros:
                    BL.instance().sorosgale.execute(vret2)
                if not vret2 == 0 or B.typepair != 'D':
                    self.buy_gale2(B)
        else:
            if roboCtrl.instance().robo.usarsoros:
                BL.instance().sorosgale.valor_lucro = 0
            msg = 'ID:{0} GALE2 {1} ${2} - {3} {4}'.format(B.op_id, B.pair, round(float(valor), 2), Idioma.traducao('Resposta IQ:'), C)
            A.error(msg)
            print(msg)