# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: jobsplay.py
# Compiled at: 2019-07-08 19:24:18
import glob, os, sys, queue, PySimpleGUI as sg
from log.logger import *
from log.path import PathLogs
import services.scheduleservice as Agenda
from services.downloadlista import ListaSinais
import models.Operation as E
import models.roboController as roboCtrl
from models.roboController import *
from models.ThreadOperacion import *
from services.noticias import *
from services.robo import Robo as RoboIQ
from jobsplayView import JobsView, JobsViewDownload
from services.getimglogo import *
from personal import dencryptfile as Decryp
obrigarTemplate = True
if obrigarTemplate:
    nomeApp = 'Robô'
else:
    nomeApp = 'JOBsPlay'
tema = 'TealMono'
lang = 'pt-br'
afiliado = 0
versaoapp = '1.9.5'
template = None
for file in glob.glob('*.cfg'):
    template = Decryp.getTemplate(file)
    break

if template:
    afiliado = int(template['afiliado'])
    nomeApp = template['nomeApp']
    tema = template['tema']
    lang = template['lang']
    try:
        img_base64 = template['imagem']
    except:
        img_base64 = ''

elif obrigarTemplate:
    sys.exit(0)
Idioma.setlang(lang)
for file in glob.glob('*.thm'):
    tema = file.replace('.thm', '')

img_logo = os.path.join(os.getcwd(), 'logo.png')
if nomeApp == 'JOBsPlay':
    oimg = LogoImg(img_logo)
    img_base64 = oimg.imagembase64
if img_base64:
    img_logo = img_base64
elif not os.path.isfile(img_logo):
    img_logo = None
afiliado = 0
roboCtrl.instance().robo = RoboIQ(versaoapp)
cf = roboCtrl.instance().robo.loadConfig()
roboCtrl.instance().robo.setConfig(cf)
roboCtrl.instance().view = JobsView(nomeApp, tema, versaoapp, img_logo, img_base64, afiliado)
roboCtrl.instance().robo.View = roboCtrl.instance().view

def externalFunction():
    roboCtrl.instance().robo.IniciarAgendamentos()
    data = []
    for sinal in roboCtrl.instance().operContrl.agenda:
        item = ['{:03d}'.format(int(sinal.op_id)),
         sinal.programmedHour.strftime('%d/%m/%y'),
         sinal.programmedHour.strftime('%H:%M:%S'),
         sinal.pair,
         sinal.direction.upper(),
         sinal.expirationMode,
         sinal.situacao,
         '{:18.2f}'.format(float(sinal.lucro))]
        data.append(item)

    roboCtrl.instance().view.janela['-TABLE-'].update(values=data)
    roboCtrl.instance().robo.ExecutaAgendamento()


class QueueHandler(logging.Handler):

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


def LeConfig():
    roboCtrl.instance().view.janela['email'].update(roboCtrl.instance().robo.email)
    if roboCtrl.instance().robo.contareal:
        roboCtrl.instance().view.janela['contatipo'].update(value=(Idioma.traducao('Real')))
    else:
        roboCtrl.instance().view.janela['contatipo'].update(value=(Idioma.traducao('Treinamento')))
    roboCtrl.instance().view.janela['usarsoros'].update(value=(roboCtrl.instance().robo.usarsoros))
    roboCtrl.instance().view.janela['prestop'].update(value=(roboCtrl.instance().robo.prestop))
    if roboCtrl.instance().robo.esperarIQ:
        roboCtrl.instance().view.janela['esperarIQ'].update(value=(Idioma.traducao('Resultado Resp. IQ')))
    else:
        roboCtrl.instance().view.janela['esperarIQ'].update(value=(Idioma.traducao('Resultado por Taxas')))
    roboCtrl.instance().view.janela['naonoticia'].update(value=(roboCtrl.instance().robo.naonoticia))
    roboCtrl.instance().view.janela['notminantes'].update(value=(roboCtrl.instance().robo.notminantes))
    roboCtrl.instance().view.janela['notminapos'].update(value=(roboCtrl.instance().robo.notminapos))
    roboCtrl.instance().view.janela['delay'].update(value=(roboCtrl.instance().robo.delay))
    if roboCtrl.instance().robo.priorid == 0:
        roboCtrl.instance().view.janela['priorid'].update(value=(Idioma.traducao('Maior Payout')))
    elif roboCtrl.instance().robo.priorid == 1:
        roboCtrl.instance().view.janela['priorid'].update(value=(Idioma.traducao('Digital')))
    elif roboCtrl.instance().robo.priorid == 2:
        roboCtrl.instance().view.janela['priorid'].update(value=(Idioma.traducao('Binárias')))
    roboCtrl.instance().view.janela['tendusar'].update(value=(roboCtrl.instance().robo.tendusar))
    roboCtrl.instance().view.janela['tendvelas'].update(value=(roboCtrl.instance().robo.tendvelas))
    roboCtrl.instance().view.janela['valinic'].update(value=(roboCtrl.instance().robo.valorinicial))
    roboCtrl.instance().view.janela['payout'].update(value=(roboCtrl.instance().robo.payoutmin))
    roboCtrl.instance().view.janela['qtdgale'].update(value=(roboCtrl.instance().robo.qtdgales))
    if roboCtrl.instance().robo.ent_tipo == 'P':
        roboCtrl.instance().view.janela['percent'].update(value=(Idioma.traducao('Percentual')))
    else:
        roboCtrl.instance().view.janela['percent'].update(value=(Idioma.traducao('Valor')))
    roboCtrl.instance().view.janela['valor1'].update(value=(roboCtrl.instance().robo.ent_valor1))
    roboCtrl.instance().view.janela['gale1'].update(value=(roboCtrl.instance().robo.ent_gale1))
    roboCtrl.instance().view.janela['gale2'].update(value=(roboCtrl.instance().robo.ent_gale2))
    roboCtrl.instance().view.janela['percentsoros'].update(value=(roboCtrl.instance().robo.percent))
    if roboCtrl.instance().robo.modelo == 'A':
        roboCtrl.instance().view.janela['modelo'].update(value=(Idioma.traducao('Agressivo')))
    elif roboCtrl.instance().robo.modelo == 'M':
        roboCtrl.instance().view.janela['modelo'].update(value=(Idioma.traducao('Moderado')))
    elif roboCtrl.instance().robo.modelo == 'C':
        roboCtrl.instance().view.janela['modelo'].update(value=(Idioma.traducao('Conservador')))
    if roboCtrl.instance().robo.tipostop == 'P':
        roboCtrl.instance().view.janela['tipostop'].update(value=(Idioma.traducao('Percentual')))
    else:
        roboCtrl.instance().view.janela['tipostop'].update(value=(Idioma.traducao('Valor')))
    roboCtrl.instance().view.janela['stopgain'].update(value=(roboCtrl.instance().robo.stopgain))
    roboCtrl.instance().view.janela['stoploss'].update(value=(roboCtrl.instance().robo.stoploss))
    ZeraPlacarTotal()
    roboCtrl.instance().view.janela['-Parar-'].update(disabled=True)
    getNoticias()
    roboCtrl.instance().view.janela.Refresh()


def ZeraPlacarTotal():
    roboCtrl.instance().operContrl.zerar()
    roboCtrl.instance().view.janela['saldoatual'].update(value=0.0)
    roboCtrl.instance().view.janela['stopgainp'].update(value=0)
    roboCtrl.instance().view.janela['stopgainv'].update(value=0.0)
    roboCtrl.instance().view.janela['stoplossp'].update(value=0)
    roboCtrl.instance().view.janela['stoplossv'].update(value=0.0)
    roboCtrl.instance().view.janela['valorinic'].update(value=0.0)
    roboCtrl.instance().view.janela['placarW'].update(value=0)
    roboCtrl.instance().view.janela['placarH'].update(value=0)
    roboCtrl.instance().view.janela['assertividade'].update(value=0.0)
    roboCtrl.instance().view.janela['saldolucro'].update(value=0.0)
    roboCtrl.instance().view.janela.Refresh()


def GravaConfig(values):

    def tratarFloat(value: str):
        try:
            return float(value)
        except:
            return 0

    if values['usarsoros'] == True:
        roboCtrl.instance().robo.usarsoros = True
    else:
        roboCtrl.instance().robo.usarsoros = False
    if values['prestop'] == True:
        roboCtrl.instance().robo.prestop = True
    else:
        roboCtrl.instance().robo.prestop = False
    if values['esperarIQ'] == Idioma.traducao('Resultado por Taxas'):
        roboCtrl.instance().robo.esperarIQ = False
    elif values['esperarIQ'] == Idioma.traducao('Resultado Resp. IQ'):
        roboCtrl.instance().robo.esperarIQ = True
    if values['naonoticia'] == True:
        roboCtrl.instance().robo.naonoticia = True
    else:
        roboCtrl.instance().robo.naonoticia = False
    roboCtrl.instance().robo.notminantes = int(tratarFloat(values['notminantes']))
    roboCtrl.instance().robo.notminapos = int(tratarFloat(values['notminapos']))
    roboCtrl.instance().robo.delay = int(tratarFloat(values['delay']))
    if values['priorid'] == Idioma.traducao('Maior Payout'):
        roboCtrl.instance().robo.priorid = 0
    elif values['priorid'] == Idioma.traducao('Digital'):
        roboCtrl.instance().robo.priorid = 1
    elif values['priorid'] == Idioma.traducao('Binárias'):
        roboCtrl.instance().robo.priorid = 2
    if values['tendusar'] == True:
        roboCtrl.instance().robo.tendusar = True
    else:
        roboCtrl.instance().robo.tendusar = False
    roboCtrl.instance().robo.tendvelas = int(tratarFloat(values['tendvelas']))
    if tratarFloat(values['valinic']) == 0:
        raise Exception(Idioma.traducao('Saldo Inicial não pode ser zero.'))
    if tratarFloat(values['payout']) == 0:
        raise Exception(Idioma.traducao('Payout não pode ser zero.'))
    roboCtrl.instance().robo.valorinicial = tratarFloat(values['valinic'])
    roboCtrl.instance().robo.payoutmin = int(tratarFloat(values['payout']))
    roboCtrl.instance().robo.qtdgales = int(tratarFloat(values['qtdgale']))
    if values['percent'] == Idioma.traducao('Percentual'):
        roboCtrl.instance().robo.ent_tipo = 'P'
    else:
        roboCtrl.instance().robo.ent_tipo = 'V'
    roboCtrl.instance().robo.ent_valor1 = tratarFloat(values['valor1'])
    roboCtrl.instance().robo.ent_gale1 = tratarFloat(values['gale1'])
    roboCtrl.instance().robo.ent_gale2 = tratarFloat(values['gale2'])
    roboCtrl.instance().robo.percent = tratarFloat(values['percentsoros'])
    if values['modelo'] == Idioma.traducao('Agressivo'):
        roboCtrl.instance().robo.modelo = 'A'
    elif values['modelo'] == Idioma.traducao('Moderado'):
        roboCtrl.instance().robo.modelo = 'M'
    if values['modelo'] == Idioma.traducao('Conservador'):
        roboCtrl.instance().robo.modelo = 'C'
    if values['tipostop'] == Idioma.traducao('Percentual'):
        roboCtrl.instance().robo.tipostop = 'P'
    else:
        roboCtrl.instance().robo.tipostop = 'V'
    if tratarFloat(values['stopgain']) == 0:
        raise Exception(Idioma.traducao('Valor do Stop Gain não pode ser zero.'))
    if tratarFloat(values['stoploss']) == 0:
        raise Exception(Idioma.traducao('Valor do Stop Loss não pode ser zero.'))
    if tratarFloat(values['stoploss']) > 100:
        if roboCtrl.instance().robo.tipostop == 'P':
            raise Exception(Idioma.traducao('Valor do Stop Loss não pode ser maior do que 100%.'))
    if tratarFloat(values['stoploss']) > tratarFloat(values['valinic']):
        if roboCtrl.instance().robo.tipostop == 'V':
            raise Exception(Idioma.traducao('Valor do Stop Loss não pode ser maior do que o Saldo Inicial.'))
    roboCtrl.instance().robo.stopgain = tratarFloat(values['stopgain'])
    roboCtrl.instance().robo.stoploss = tratarFloat(values['stoploss'])
    roboCtrl.instance().robo.saveConfig()
    cf = roboCtrl.instance().robo.loadConfig()
    roboCtrl.instance().robo.setConfig(cf)


def GravaConfigTP(email, contatipo):
    contareal = False
    if contatipo == Idioma.traducao('Real'):
        contareal = True
    roboCtrl.instance().robo.saveConfigTP(email, contareal)
    cf = roboCtrl.instance().robo.loadConfig()
    roboCtrl.instance().robo.setConfig(cf)


def validarEditsNumeros(editname: str, values):
    try:
        if len(values[editname]):
            if values[editname][(-1)] not in '0123456789.':
                roboCtrl.instance().view.janela[editname].update(values[editname][:-1])
    except:
        pass


def cancelSinal(item):
    i = 0
    for sinal in roboCtrl.instance().operContrl.agenda:
        if i == item:
            Agenda.cancelId(sinal.op_id)
            msg = 'ID:{0} {1} {2} Cancelado Sobreposto'.format(sinal.op_id, sinal.pair, sinal.programmedHour.strftime('%H:%M:%S'))
            logger.warning(msg)
            print(msg)
            break
        else:
            i += 1


def Habilitar(iniciado: bool):
    roboCtrl.instance().view.janela['-Iniciar-'].update(disabled=iniciado)
    roboCtrl.instance().view.janela['-Parar-'].update(disabled=(not iniciado))
    roboCtrl.instance().view.janela['-Gravar-'].update(disabled=iniciado)
    roboCtrl.instance().view.janela['-Download-'].update(disabled=iniciado)
    roboCtrl.instance().view.janela['-abrirlista-'].update(disabled=iniciado)
    roboCtrl.instance().view.janela['email'].update(disabled=iniciado)
    roboCtrl.instance().view.janela['senha'].update(disabled=iniciado)
    roboCtrl.instance().view.janela['contatipo'].update(disabled=iniciado)


def main():
    global afiliado
    roboCtrl.instance().view.Show()
    logging.basicConfig(level=(logging.DEBUG))
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)
    LeConfig()
    janelaDown = False
    while 1:
        event, values = roboCtrl.instance().view.janela.Read()
        if event == None:
            break
        else:
            if event == 'valinic':
                validarEditsNumeros('valinic', values)
            if event == 'delay':
                validarEditsNumeros('delay', values)
            if event == 'payout':
                validarEditsNumeros('payout', values)
            if event == 'qtdgale':
                validarEditsNumeros('qtdgale', values)
            if event == 'valor1':
                validarEditsNumeros('valor1', values)
            if event == 'gale1':
                validarEditsNumeros('gale1', values)
            if event == 'gale2':
                validarEditsNumeros('gale2', values)
            if event == 'percentsoros':
                validarEditsNumeros('percentsoros', values)
            if event == 'stopgain':
                validarEditsNumeros('stopgain', values)
            if event == 'stoploss':
                validarEditsNumeros('stoploss', values)
            if event == '-Iniciar-' and not roboCtrl.instance().view.appStarted:
                try:
                    valido = True
                    if values['senha'] == '':
                        sg.popup((Idioma.traducao('Informe sua senha.')), no_titlebar=True,
                          keep_on_top=True,
                          text_color='black',
                          background_color='#DFDDDD')
                        valido = False
                    if not os.path.isfile(values['arqlista']):
                        if valido:
                            sg.popup((Idioma.traducao('Arquivo da lista não foi localizado.')), no_titlebar=True,
                              keep_on_top=True,
                              text_color='black',
                              background_color='#DFDDDD')
                            valido = False
                    if valido:
                        GravaConfigTP(values['email'], values['contatipo'])
                        roboCtrl.instance().robo.senha = values['senha']
                        ZeraPlacarTotal()
                        threadedApp = ThreadOper(target=externalFunction)
                        roboCtrl.instance().add_listThread = threadedApp
                        appStarted = True
                        roboCtrl.instance().robo.arqLista = values['arqlista']
                        if roboCtrl.instance().robo.Conectar():
                            Habilitar(True)
                            if not threadedApp.is_alive():
                                threadedApp.start()
                except Exception as inst:
                    try:
                        print(inst)
                        sg.popup_error((str(inst)), no_titlebar=True,
                          keep_on_top=True,
                          text_color='black',
                          background_color='#DFDDDD')
                    finally:
                        inst = None
                        del inst

            if event == '-Gravar-':
                try:
                    GravaConfig(values)
                    sg.popup((Idioma.traducao('Atenção')), (Idioma.traducao('Parâmetros gravados com sucesso!')), no_titlebar=True,
                      keep_on_top=True,
                      text_color='black',
                      background_color='#DFDDDD')
                except Exception as inst:
                    try:
                        sg.popup_error((str(inst)), no_titlebar=True,
                          keep_on_top=True,
                          text_color='black',
                          background_color='#DFDDDD')
                    finally:
                        inst = None
                        del inst

                if event == '-Ajuda-':
                    Leiame = Idioma.traducaoLeiame()
                    sg.popup_scrolled((Idioma.traducao('Leiame')), Leiame, size=(120,
                                                                                 20), font=('Helvetica',
                                                                                            8),
                      no_titlebar=True,
                      keep_on_top=True,
                      text_color='black',
                      background_color='#DFDDDD')
                if event == '-TABLE-':
                    try:
                        item = int(values['-TABLE-'][0])
                        cancelitem = sg.popup_yes_no((Idioma.traducao('Cancelar este sinal?')), no_titlebar=True,
                          keep_on_top=True,
                          text_color='black',
                          background_color='#DFDDDD')
                        if cancelitem == 'Yes':
                            cancelSinal(item)
                    except:
                        pass

        if event == '-Download-':
            if not janelaDown:
                janelaDown = True
                roboCtrl.instance().view.janela['-Iniciar-'].update(disabled=True)
                roboCtrl.instance().view.janela['-Parar-'].update(disabled=True)
                roboCtrl.instance().view.janela['-abrirlista-'].update(disabled=True)
                viewDown = JobsViewDownload()
                viewDown.Show()
                wslista = ListaSinais()
                wslista.getLista(afiliado)
                viewDown.atualizaGrid(wslista.lista)
            if janelaDown:
                ev2, vals2 = viewDown.janela.read()
                if ev2 is None or ev2 == '-CancLista-':
                    janelaDown = False
                    roboCtrl.instance().view.janela['-Iniciar-'].update(disabled=False)
                    roboCtrl.instance().view.janela['-Parar-'].update(disabled=True)
                    roboCtrl.instance().view.janela['-abrirlista-'].update(disabled=False)
                    viewDown.janela.close()
                if ev2 == '-ConfLista-':
                    janelaDown = False
                    try:
                        idx = int(vals2['-TABLELISTA-'][0])
                        nomelista = os.path.join(os.getcwd(), 'downloads')
                        PathLogs.create_dir(nomelista)
                        arq = wslista.lista[idx]['id'] + '_' + wslista.lista[idx]['data'] + '_' + wslista.lista[idx]['nome'] + '.txt'
                        arq = arq.replace('-', '_')
                        arq = arq.replace(' ', '_')
                        nomelista = os.path.join(nomelista, arq)
                        arqlista = wslista.getArquivo(int(wslista.lista[idx]['id']))
                        if arqlista:
                            with open(nomelista, 'wb') as f:
                                f.write(arqlista)
                            roboCtrl.instance().view.janela['arqlista'].update(value=nomelista)
                    except Exception as inst:
                        try:
                            print(inst)
                            sg.popup_error((str(inst)), no_titlebar=True,
                              keep_on_top=True,
                              text_color='black',
                              background_color='#DFDDDD')
                        finally:
                            inst = None
                            del inst

                    roboCtrl.instance().view.janela['-Iniciar-'].update(disabled=False)
                    roboCtrl.instance().view.janela['-Parar-'].update(disabled=True)
                    roboCtrl.instance().view.janela['-abrirlista-'].update(disabled=False)
                    viewDown.janela.close()
            if event in ('-Parar-', '-Fechar-'):
                if Agenda.cancel(0):
                    appStarted = False
                    roboCtrl.instance().robo.PararTudo()
                    for th in roboCtrl.instance().add_listThread:
                        if th.isAlive():
                            th.stop()

                    if event == '-Parar-':
                        print(Idioma.traducao('Agendamentos cancelados com sucesso!'))
                        print('====================================')
                        Habilitar(False)
                if event == '-Fechar-':
                    break
            try:
                record = log_queue.get(block=False)
            except queue.Empty:
                pass
            else:
                msg = queue_handler.format(record)

    roboCtrl.instance().view.janela.close()
    del roboCtrl.instance().view.janela


if __name__ == '__main__':
    main()
# global lang ## Warning: Unused global
# global nomeApp ## Warning: Unused global
# global tema ## Warning: Unused global
# global versaoapp ## Warning: Unused global