# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: jobsplayView.py
# Compiled at: 2019-07-08 19:24:18
import sys, os, PySimpleGUI as sg
from models.roboController import *

class JobsViewDownload:

    def __init__(self):
        self.headings = [
         Idioma.traducao('Data'),
         Idioma.traducao('Lista')]
        self.data = [['' for _ in range(len(self.headings))]]
        self.layout = [
         [
          sg.Text('Lista de Sinais', size=(20, 0), key='cabec', justification='l', font=('Helvetica',
                                                                               8,
                                                                               'bold'), text_color=(sg.theme_text_color()),
            background_color=(sg.theme_background_color()))],
         [
          sg.Table(values=(self.data), headings=(self.headings), background_color='white',
            header_font=('Helvetica', 8, 'bold'),
            justification='center',
            auto_size_columns=False,
            col_widths=(8, 25),
            num_rows=5,
            pad=(0, 0),
            key='-TABLELISTA-')],
         [
          sg.Button((Idioma.traducao('Confirmar')), size=(20, 1), key='-ConfLista-'),
          sg.Button((Idioma.traducao('Cancelar')), size=(20, 1), key='-CancLista-')]]

    def Show(self):
        sg.set_options(text_element_background_color=(sg.theme_input_text_color()), element_background_color=(sg.theme_input_background_color()),
          input_elements_background_color=(sg.theme_input_background_color()))
        self.janela = sg.Window('Lista de Sinais', (self.layout), font=('Helvetica',
                                                                        8),
          margins=(0, 0),
          text_justification='r',
          finalize=True,
          return_keyboard_events=True,
          keep_on_top=True,
          force_toplevel=True,
          no_titlebar=True,
          grab_anywhere=False)
        for col in ('cabec', '-TABLELISTA-'):
            self.janela[col].expand(expand_x=True)

    def atualizaGrid(self, datalista):
        data = []
        for item in datalista:
            data.append([item['data'], item['nome']])

        self.janela['-TABLELISTA-'].update(values=data)
        self.janela.refresh()


class JobsView:

    def __init__(self, nomeapp='JOBsPlay', tema='Reddit', versao='', img_logo=None, img_base64=None, afiliado=0):
        self.appStarted = False
        self.nomeApp = nomeapp
        self.versao = Idioma.traducao('Versão') + ' ' + versao
        sg.theme(tema)
        self.headings = [
         'ID',
         Idioma.traducao('Data'),
         Idioma.traducao('Horário'),
         Idioma.traducao('Ativo'),
         Idioma.traducao('Direção'),
         Idioma.traducao('Dur.'),
         Idioma.traducao('Situação'),
         Idioma.traducao('Lucro')]
        self.data = [['' for _ in range(len(self.headings))]]
        self.headings2 = [
         Idioma.traducao('Horário'),
         Idioma.traducao('Moeda'),
         Idioma.traducao('Notícias (3 Touros)')]
        self.data2 = [['' for _ in range(len(self.headings2))]]
        self.col01 = sg.Column([
         [
          sg.Frame((Idioma.traducao('Opções')), [
           [
            sg.Checkbox((Idioma.traducao('Usar SorosGale')), key='usarsoros')],
           [
            sg.Checkbox((Idioma.traducao('Usar Pré Stop Loss')), key='prestop')],
           [
            sg.Text(Idioma.traducao('Aguardar')),
            sg.OptionMenu(values=(Idioma.traducao('Resultado por Taxas'), Idioma.traducao('Resultado Resp. IQ')), key='esperarIQ')],
           [
            sg.Text('Delay (seg)', size=(14, 0)), sg.Spin(values=[i for i in range(0, 11)], initial_value=0, enable_events=True, key='delay')],
           [
            sg.Text((Idioma.traducao('Prioridade')), size=(14, 0)),
            sg.OptionMenu(values=(Idioma.traducao('Maior Payout'), Idioma.traducao('Digital'), Idioma.traducao('Binárias')), key='priorid')],
           [
            sg.Frame((Idioma.traducao('Notícias')), [
             [
              sg.Checkbox((Idioma.traducao('Não Operar em Notícias')), key='naonoticia')],
             [
              sg.Text((Idioma.traducao('Minutos (Antes)')), size=(13, 0)), sg.Spin(values=[i for i in range(0, 60)], initial_value=0, enable_events=True, key='notminantes')],
             [
              sg.Text((Idioma.traducao('Minutos (Após)')), size=(13, 0)), sg.Spin(values=[i for i in range(0, 60)], initial_value=0, enable_events=True, key='notminapos')]],
              key='-framenoticia-')],
           [
            sg.Frame((Idioma.traducao('Tendência')), [
             [
              sg.Checkbox((Idioma.traducao('Não Operar Contra')), key='tendusar')],
             [
              sg.Text((Idioma.traducao('Quant. Velas')), size=(13, 0)), sg.Spin(values=[i for i in range(0, 100)], initial_value=0, enable_events=True, key='tendvelas')]],
              key='-frametend-')]],
            key='-frameopcao-')]],
          key='-tab1col01-',
          pad=(0, 0),
          justification='left',
          element_justification='left')
        self.col02 = sg.Column([
         [
          sg.Frame('', [
           [
            sg.Frame('', [
             [
              sg.Text((Idioma.traducao('Saldo Inicial $')), size=(15, 0), font=('Helvetica', 9, 'bold')),
              sg.InputText(size=(13, 0), font=('Helvetica', 9, 'bold'), justification='right', enable_events=True, key='valinic')]],
              key='-framevalinic-')],
           [
            sg.Frame((Idioma.traducao('Opções de Entrada')), [
             [
              sg.Text((Idioma.traducao('Payout Mínimo %')), size=(17, 0)),
              sg.Spin(values=[i for i in range(50, 99)], initial_value=80, size=(13, 1), enable_events=True, key='payout')],
             [
              sg.Text((Idioma.traducao('Qtd. Gales')), size=(17, 0)),
              sg.Spin(values=[i for i in range(0, 3)], initial_value=0, size=(13, 1), enable_events=True, key='qtdgale')],
             [
              sg.Text((Idioma.traducao('Tipo de Stop')), size=(17, 0)),
              sg.OptionMenu(values=(Idioma.traducao('Percentual'), Idioma.traducao('Valor')), size=(9,
                                                                                      1), key='tipostop')],
             [
              sg.Text('Stop Gain $', size=(17, 0)),
              sg.InputText(size=(15, 0), justification='right', enable_events=True, key='stopgain')],
             [
              sg.Text('Stop Loss $', size=(17, 0)),
              sg.InputText(size=(15, 0), justification='right', enable_events=True, key='stoploss')]],
              key='-frameopcent-')]],
            key='-frameentinicial-')]],
          key='-tab1col02-',
          pad=(0, 0),
          justification='left',
          element_justification='left')
        self.col03 = sg.Column([
         [
          sg.Frame((Idioma.traducao('Entradas Fixas')), [
           [
            sg.Text((Idioma.traducao('Tipo')), size=(10, 0)),
            sg.OptionMenu(values=(Idioma.traducao('Percentual'), Idioma.traducao('Valor')), size=(15,
                                                                                      1), key='percent')],
           [
            sg.Text((Idioma.traducao('1ª Entrada $')), size=(10, 0)),
            sg.InputText(size=(15, 0), justification='right', enable_events=True, key='valor1')],
           [
            sg.Text((Idioma.traducao('Gale 1 $')), size=(10, 0)),
            sg.InputText(size=(15, 0), justification='right', enable_events=True, key='gale1')],
           [
            sg.Text((Idioma.traducao('Gale 2 $')), size=(10, 0)),
            sg.InputText(size=(15, 0), justification='right', enable_events=True, key='gale2')]],
            key='-frameentfixa-')]],
          key='-tab1col03-',
          pad=(0, 0),
          justification='left',
          element_justification='left')
        self.col04 = sg.Column([
         [
          sg.Frame('SorosGale', [
           [
            sg.Text(Idioma.traducao('1ª Entrada %')),
            sg.InputText(size=(15, 0), justification='right', enable_events=True, key='percentsoros')],
           [
            sg.Text(Idioma.traducao('Modelo')),
            sg.OptionMenu(values=(Idioma.traducao('Agressivo'), Idioma.traducao('Moderado'), Idioma.traducao('Conservador')), size=(15,
                                                                                                                        1), key='modelo')],
           [
            sg.Text((Idioma.traducao('Horário sobrepostos serão cancelados automáticamente')), size=(30,
                                                                                         3))]],
            key='-framesoros-')]],
          key='-tab1col04-',
          pad=(0, 0),
          justification='left',
          element_justification='left')
        self.layout_tab1 = [
         [
          self.col01, self.col02, self.col03, self.col04],
         [
          sg.Button((Idioma.traducao('Gravar')), size=(20, 1), key='-Gravar-'),
          sg.Text('', size=(100, 2)),
          sg.Button((Idioma.traducao('Leiame')), size=(20, 1), key='-Ajuda-')]]
        if img_base64:
            self.imglogo = sg.Image(data=img_base64, size=(300, 130), key='-imglogo-')
        elif img_logo:
            self.imglogo = sg.Image(img_logo, size=(300, 130), key='-imglogo-')
        else:
            self.imglogo = sg.Frame('', [], size=(305, 130), pad=(0, 0), key='-imglogo-')
        self.col1 = sg.Column([
         [
          self.imglogo],
         [
          sg.Frame('', [
           [
            sg.Text('Email', size=(8, 0), font=('Helvetica', 8, 'bold')),
            sg.InputText(size=(20, 0), key='email')],
           [
            sg.Text((Idioma.traducao('Senha')), size=(8, 0), font=('Helvetica', 8, 'bold')),
            sg.Input(size=(20, 0), password_char='*', key='senha')],
           [
            sg.Text((Idioma.traducao('Conta')), size=(8, 0), font=('Helvetica', 8, 'bold')),
            sg.OptionMenu(values=(Idioma.traducao('Treinamento'), Idioma.traducao('Real')), size=(20,
                                                                                      1), key='contatipo')]],
            pad=(0, 0),
            key='-framelogin-')],
         [
          sg.Frame('', [
           [
            sg.Text((Idioma.traducao('Saldo Atual $')), size=(18, 0), font=('Helvetica', 8, 'bold'), justification='rigth'),
            sg.Text(size=(10, 0), relief='sunken', font=('Helvetica', 8, 'bold'), justification='right', key='saldoatual')],
           [
            sg.Text('Stop Gain %', font=('Helvetica', 8, 'bold'), size=(10, 0)),
            sg.Text(size=(4, 0), relief='sunken', font=('Helvetica', 8, 'bold'), justification='right', key='stopgainp'),
            sg.Text('$', font=('Helvetica', 8, 'bold'), size=(1, 0), justification='right'),
            sg.Text(size=(10, 0), relief='sunken', font=('Helvetica', 8, 'bold'), justification='right', key='stopgainv')],
           [
            sg.Text('Stop Loss %', font=('Helvetica', 8, 'bold'), text_color='red', size=(10, 0)),
            sg.Text(size=(4, 0), relief='sunken', font=('Helvetica', 8, 'bold'), text_color='red', justification='right', key='stoplossp'),
            sg.Text('$', font=('Helvetica', 8, 'bold'), size=(1, 0), justification='right'),
            sg.Text(size=(10, 0), relief='sunken', font=('Helvetica', 8, 'bold'), text_color='red', justification='right', key='stoplossv')]],
            pad=(0, 0),
            key='-framesaldo-')],
         [
          sg.Frame('', [
           [
            sg.Text((Idioma.traducao('Saldo Inicial $')), size=(26, 0), font=('Helvetica', 8, 'bold'), justification='rigth'),
            sg.Text(size=(8, 0), relief='sunken', font=('Helvetica', 8, 'bold'), justification='right', key='valorinic')],
           [
            sg.Text('WIN', size=(3, 0), font=('Helvetica', 8, 'bold')),
            sg.Text(size=(7, 0), relief='sunken', font=('Helvetica', 8, 'bold'), justification='right', key='placarW'),
            sg.Text((Idioma.traducao('Assertividade %')), font=('Helvetica', 8, 'bold'), size=(13,
                                                                                   0), justification='right'),
            sg.Text(size=(8, 0), relief='sunken', font=('Helvetica', 8, 'bold'), justification='right', key='assertividade')],
           [
            sg.Text('HIT', size=(3, 0), font=('Helvetica', 8, 'bold'), text_color='red'),
            sg.Text(size=(7, 0), relief='sunken', font=('Helvetica', 8, 'bold'), text_color='red', justification='right', key='placarH'),
            sg.Text((Idioma.traducao('Lucro/Perda $')), font=('Helvetica', 8, 'bold'), size=(13,
                                                                                 0), justification='right'),
            sg.Text(size=(8, 0), relief='sunken', font=('Helvetica', 8, 'bold'), justification='right', key='saldolucro')]],
            pad=(0, 0),
            key='-frameplacar-')],
         [
          sg.Table(values=(self.data2), headings=(self.headings2), background_color='white',
            header_font=('Helvetica', 8, 'bold'),
            justification='center',
            auto_size_columns=False,
            col_widths=(4, 4, 19),
            num_rows=7,
            pad=(0, 0),
            key='-TABLENOTICIAS-')],
         [
          sg.Text('Licença:', size=(50, 1), text_color='green', pad=(0, 0), key='-licenca-', justification='left')]],
          key='-tab2col1-',
          justification='left',
          element_justification='left')
        self.col2 = sg.Column([
         [
          sg.Text(Idioma.traducao('Lista (txt)')),
          sg.Input(size=(30, 0), key='arqlista'),
          sg.FileBrowse((Idioma.traducao('Abrir')), size=(7, 1), key='-abrirlista-', file_types=(('Lista de sinais', '*.txt'), )),
          sg.Button('Download', size=(10, 1), key='-Download-', visible=(afiliado > 0))],
         [
          sg.Button((Idioma.traducao('Iniciar')), size=(20, 1), font=('Helvetica', 10, 'bold'), bind_return_key=True, button_color=('white',
                                                                                                                          'springgreen4'), key='-Iniciar-'),
          sg.Button((Idioma.traducao('Parar')), size=(20, 1), font=('Helvetica', 10, 'bold'), button_color=('white',
                                                                                                  'firebrick3'), key='-Parar-')],
         [
          sg.Table(values=(self.data), headings=(self.headings), background_color='white',
            header_font=('Helvetica', 8, 'bold'),
            justification='center',
            auto_size_columns=False,
            col_widths=(4, 6, 6, 8, 5, 4, 11, 8),
            num_rows=19,
            enable_events=False,
            bind_return_key=True,
            key='-TABLE-')],
         [
          sg.Output(size=(57, 6), font=('Courier New', 8), pad=(0, 0), background_color='black',
            text_color='white',
            key='-output-')]],
          key='-tab2col2-',
          justification='left',
          element_justification='left')
        self.layout_tab2 = [
         [
          self.col1, self.col2]]
        self.layout = [
         [
          sg.TabGroup([
           [
            sg.Tab(Idioma.traducao('Lista de Sinais'), self.layout_tab2),
            sg.Tab(Idioma.traducao('Configurações'), self.layout_tab1)]],
            pad=(0, 0),
            key='--tabgroup1')],
         [
          sg.Text('', size=(50, 1), text_color='red', justification='left', key='-status-'),
          sg.Button((Idioma.traducao('Fechar')), size=(20, 1), font=('Helvetica', 10, 'bold'), key='-Fechar-')]]

    def Show(self):
        sg.set_options(text_element_background_color=(sg.theme_input_text_color()), element_background_color=(sg.theme_input_background_color()),
          input_elements_background_color=(sg.theme_input_background_color()))
        self.janela = sg.Window((self.nomeApp + ' - ' + self.versao), (self.layout), font=('Helvetica',
                                                                                           8),
          margins=(0, 0),
          finalize=True,
          disable_close=True,
          alpha_channel=0.9,
          icon='./icon/jobsplay.ico')
        for col in ('-status-', 'saldoatual', 'valorinic', '-TABLENOTICIAS-', '-licenca-',
                    '-status-', 'email', 'senha', 'contatipo', 'stopgainv', 'stoplossv',
                    'assertividade', 'saldolucro', 'valinic', 'payout', 'qtdgale',
                    'tipostop', 'stopgain', 'stoploss', 'percent', 'valor1', 'gale1',
                    'gale2', 'percentsoros', 'modelo', 'priorid', 'delay', 'notminantes',
                    'notminapos', 'tendvelas', '-framenoticia-', '-frametend-', 'arqlista',
                    '-Iniciar-', '-Parar-'):
            self.janela[col].expand(expand_x=True)

        for col in ('-frameopcao-', '-frameentinicial-', '-frameentfixa-', '-framesoros-'):
            self.janela[col].expand(expand_y=True)

        for col in ('-framelogin-', '-framesaldo-', '-frameplacar-', '-output-', '-tab2col2-',
                    '-TABLE-'):
            self.janela[col].expand(expand_y=True, expand_x=True)


def ExemploCriarNovoTema():
    sg.LOOK_AND_FEEL_TABLE['MyNewTheme'] = {'BACKGROUND':'#3d4854', 
     'TEXT':'white', 
     'INPUT':'white', 
     'TEXT_INPUT':'#000000', 
     'SCROLL':'#c7e78b', 
     'BUTTON':('white', '#3d4854'), 
     'PROGRESS':('#01826B', '#D0D0D0'), 
     'BORDER':1, 
     'SLIDER_DEPTH':0,  'PROGRESS_DEPTH':0}
    sg.theme('MyNewTheme')