# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: models\Traducao.py
# Compiled at: 2019-07-08 19:24:18


class Traduzir:

    def __init__(self, lang='pt-br'):
        self.lang = lang.lower()
        self.textos_pt_br = [
         'Versão',
         'Agendado',
         'Real',
         'Treinamento',
         'Percentual',
         'Valor',
         'Agressivo',
         'Moderado',
         'Conservador',
         'Informe sua senha.',
         'Arquivo da lista não foi localizado.',
         'Atenção',
         'Parâmetros gravados com sucesso!',
         'Agendamentos cancelados com sucesso!',
         'Arquivo não localizado na pasta.',
         'Lista vazia ou com dia/horário expirados.',
         'Aguarde, conectando a IQ...',
         'Tipo de conta:',
         'Parâmetros iniciais:',
         'Valor inicial: $',
         'Quantidade de gales:',
         'Payout mínimo:',
         'Pré-Stop Loss: Ligado',
         'Não operar em notícia',
         'Entradas fixas:',
         'Entrada: $',
         'Gale 1: $',
         'Gale 2: $',
         'Modelo: Agressivo',
         'Modelo: Moderado',
         'Modelo: Conservador',
         '1ª entrada: %',
         'Valor: $',
         'Parar de operar quando atingir: $',
         'Parar de operar quando atingir: $',
         'Agendamento realizado com sucesso!',
         'Abrir',
         'Data',
         'Horário',
         'Ativo',
         'Direção',
         'Dur.',
         'Situação',
         'Lucro',
         'Moeda',
         'Notícias (3 Touros)',
         'Opções',
         'Usar SorosGale',
         'Usar Pré Stop Loss',
         'Não Operar em Notícias',
         'Opções de Entrada',
         'Saldo Inicial $',
         'Payout mínimo %',
         'Qtd. Gales',
         'Tipo de Stop',
         'Entradas Fixas',
         'Tipo',
         '1ª Entrada $',
         'Gale 1 $',
         'Gale 2 $',
         '1ª Entrada %',
         'Modelo',
         'Gravar',
         'Senha',
         'Conta',
         'Saldo Atual $',
         'Assertividade %',
         'Lucro/Perda $',
         'Lista (txt)',
         'Iniciar',
         'Parar',
         'Fechar',
         'Lista de Sinais',
         'Configurações',
         'Diferenca de horario:',
         'Problema na conexão, verifique sua internet.',
         'Login/Senha inválido.',
         'Conta conectada:',
         'Fechado',
         'Aberto',
         'Tendência',
         'Cancelado',
         'Erro... Não houve comunição com servidor para validar sua licença. Código',
         'Sua licença expirou dia {}',
         'Sua licença vai expirar dia {}\nNão esqueça de renová-la!',
         'Licença: {} até {}',
         'Licença inválida. Não existe para este email ou está cancelada.',
         'Erro... Não houve comunição com servidor para validar sua licença.',
         'Queda de Internet durante a Operacao',
         'Lucro atual: $',
         'Lucro previsto: $',
         'inválido para a moeda',
         'mínimo de $',
         'Contra Têndencia',
         'Existe notícia de 3 touros',
         'Notícia',
         'Payout inferior:',
         'atual:',
         '1ª Entrada',
         'Perdeu: $',
         'Ganhou: $',
         'Resposta IQ:',
         'Notícias',
         'Minutos (Antes)',
         'Minutos (Após)',
         'Layout inválido.\nLayout correto: ATIVO;DIA;HORARIO;DIRECAO;DURACAO',
         'Leiame',
         'Prioridade',
         'Digital',
         'Binárias',
         'Maior Payout',
         'Não Operar Contra',
         'Quant. Velas',
         'Horário sobrepostos serão cancelados automáticamente',
         'Cancelar este sinal?',
         'Usar EMA5 + SMA20',
         'Aguardar',
         'Resultado por Taxas',
         'Resultado Resp. IQ',
         'Expiração Indisponível',
         'Saldo Inicial não pode ser zero.',
         'Payout não pode ser zero.',
         'Valor do Stop Gain não pode ser zero.',
         'Valor do Stop Loss não pode ser zero.',
         'Valor do Stop Loss não pode ser maior do que 100%.',
         'Valor do Stop Loss não pode ser maior do que o Saldo Inicial.']
        self.textos_ing = [
         'Version',
         'Scheduled',
         'Real',
         'Training',
         'Percent',
         'Value',
         'Aggressive',
         'Moderate',
         'Conservative',
         'Inform your password.',
         'List file not found.',
         'Attention',
         'Parameters successfully saved!',
         'Schedules canceled successfully!',
         'File not found in the folder.',
         'List empty or with expired day / time.',
         'Wait, connecting the IQ ...',
         'Account Type:',
         'Initial parameters:',
         'Starting value: $',
         'Number of Steps:',
         'Minimum payout:',
         'Pre-Stop Loss: On',
         'Do not operate on news',
         'Fixed inputs:',
         'Entry: $',
         'Step 1: $',
         'Step 2: $',
         'Model: Aggressive',
         'Model: Moderate',
         'Model: Conservative',
         '1st entry: %',
         'Value: $',
         'Stop trading when you reach: $',
         'Stop trading when you reach: $',
         'Scheduling successful!',
         'Open',
         'Date',
         'Time',
         'Pair',
         'Option',
         'Exp.',
         'Situation',
         'Profit',
         'Coin',
         'News (3 Bulls)',
         'Options',
         'Use Soros',
         'Use Pre Stop Loss',
         'Do not operate in News',
         'Input Options',
         'Initial Value $',
         'Minimum payout %',
         'Qty. Step',
         'Stop Type',
         'Fixed Entries',
         'Type',
         '1st Entry $',
         'Step 1 $',
         'Step 2 $',
         '1st Entry %',
         'Model',
         'Record',
         'Password',
         'Account',
         'Current Balance $',
         'Assertiveness%',
         'Profit / Loss $',
         'List (txt)',
         'Start',
         'Stop',
         'Close',
         'List of Signs',
         'Settings',
         'Time difference:',
         'Connection problem, check your internet.',
         'Invalid login / password.',
         'Connected account:',
         'Closed',
         'Open',
         'Trend',
         'Canceled',
         'Error ... There was no communication with the server to validate your license. Code',
         'Your license expired day {}',
         "Your license will expire on {}\nDon't forget to renew it!",
         'License: {} to {}',
         'Invalid license. It does not exist for this email or is canceled.',
         'Error ... There was no communication with the server to validate your license.',
         'Internet outage during Operation',
         'Current profit: $',
         'Estimated profit: $',
         'invalid for currency',
         'minimum of $',
         'Against tendency',
         'There is news of 3 bulls',
         'News',
         'Lower payout:',
         'current:',
         '1st Entry',
         'Lost: $',
         'Won: $',
         'Response from IQ:',
         'News',
         'Minutes (Before)',
         'Minutes (After)',
         'Invalid layout.\nCorrect layout: ACTIVE;DAY;TIME;DIRECTION;DURATION',
         'Read Me',
         'Priority',
         'Digital',
         'Binary',
         'Max Payout',
         'Do not Operate Against',
         'Num of Candles',
         'Overlapping schedules will be canceled automatically',
         'Cancel this signal?',
         'Use EMA5 + SMA20',
         'Wait',
         'Result by Fees',
         'Result by IQ',
         'Expiration Unavailable',
         'Opening Balance cannot be zero.',
         'Payout cannot be zero.',
         'Stop Gain value cannot be zero.',
         'Stop Loss value cannot be zero.',
         'Stop Loss value cannot be greater than 100%.',
         'Stop Loss amount cannot be greater than the Opening Balance.']

    def setlang(self, lang: str='pt-br'):
        self.lang = lang

    def traducao(self, texto: str):
        try:
            if self.lang == 'ing':
                idx = 0
                for txt in self.textos_pt_br:
                    if str(txt).lower() == texto.lower():
                        return self.textos_ing[idx]
                    else:
                        idx += 1

            else:
                return texto
        except:
            return texto

    def traducaoLeiame(self):
        texto = ''
        if self.lang == 'ing':
            texto += '\n*** Important ***\n'
            texto += 'We are an entry automation robot in Binary Operations. The execution of entry orders is completely linked to your signal list and the number of Wales requested. The gain and loss are the users responsibility. Take into account in your risk management, all the possibilities that can occur during a Trader.\n\n'
            texto += '*** List Layout Template ***\n'
            texto += 'PAIR + DAY + HOURS + DIRECTION + EXPIRATION TIME\n'
            texto += 'EX. EURUSD; 10; 15: 00; CALL; 5\n\n'
            texto += '*** Access ***\n'
            texto += 'Access to operations must be with IQ Option email and password. The access data provided is not visible to us. They are restricted to your computer only.\n\n'
            texto += '*** Options ***\n'
            texto += 'Use SorosGale: When activating this option you should be aware that the entries and Wales will be according to the percentage described in the Soros field and according to the profile: Conservative / Moderate / Aggressive.\n'
            texto += 'See the operation of each one of them through the link:\n\n'
            texto += '*** Use Pre Stop Loss ***\n'
            texto += 'When activating the Pre Stop Loss option in a situation where you are close to the Stop Loss margin, the robot interrupts operations, avoiding exceeding the stipulated Stop Loss.\n\n'
            texto += '*** Wait for Result ***\n'
            texto += 'BY FEES - We have the result by the closing rate, with this we have a smaller delay, but with the risk of the result being different from the final IQ, because in the last second it happens to change the direction of the candle.\n'
            texto += 'BY IQ RESPONSE - We have the result for the IQ response, so we have a longer delay, but the result will be 100% equal to that of IQ.\n\n'
            texto += '*** Delay ***\n'
            texto += 'You will be able to inform at what moment in a fraction of a second your order will enter. Anticipating or delaying entry.\n'
            texto += 'OBS. This option will only be valid for the first entry. From the second, it will depend on the response time of the IQ Option.\n\n'
            texto += '*** News ***\n'
            texto += 'In this, the robot will filter your entries freeing them from the news of 3 bulls listed on Investing.com\n'
            texto += 'You will also have control of how long before and after the news the robot will return to operation.\n\n'
            texto += '*** Entrance Options ***\n'
            texto += 'Initial Value: Current value of your broker or an amount you wish to work on your operations.\n'
            texto += 'Minimum Payout (%): Which acceptable minimum to carry out the operations.\n'
            texto += 'Gale Qty: How many Wales do you want to make in your operations\n'
            texto += 'Stop Loss Type:\n'
            texto += '- Percentage: The numbers in the Stop Loss and Take Profit fields will be a multiplication in percentage times the value entered in the Initial Value field.\n'
            texto += '- Value: The numbers in the Stop Loss and Take Profit fields will be fixed regardless of the value entered in the Initial Value field.\n\n'
            texto += '*** Fixed Entries ***\n'
            texto += 'Type:\n'
            texto += '- Percentage: The values \u200b\u200bof the Input 1, Gale 1, Gale 2 fields will be a multiplication in percentage times the value entered in the Value field\n'
            texto += '- Value: The values \u200b\u200bof the Input 1, Gale 1, Gale 2 fields will be fixed regardless of the value entered in the Initial Value field.\n\n'
            texto += '*** Record button ***\n'
            texto += 'The information entered and / or adjusted must be saved when clicking on the SAVE Button.\n\n'
            texto += '*** Close ***\n'
            texto += 'To close operations and the entry robot, the CLOSE button located in the lower right corner must be activated\n'
        else:
            texto += '\n*** Importante ***\n'
            texto += 'Somos um robô de automatização de entradas em Operações Binárias. A execução das ordens de entrada está totalmente ligada à sua lista de sinais e à quantidade de Gales solicitados. O ganho e perda são de responsabilidade do usuário. Leve em consideração no seu gerenciamento de risco, todas as possibilidades que podem ocorrer durante um Trader.\n\n'
            texto += '*** Modelo de Layout da Lista!!\n'
            texto += 'PAR+DIA+HORÁRIO+DIREÇÃO+TEMPO DE EXPIRAÇÃO\n'
            texto += 'EX. EURUSD;10;15:00;CALL;5\n\n'
            texto += '*** Acesso ***\n'
            texto += 'O acesso às operações deverá ser com o email e senha da IQ Option. Os dados fornecidos de acesso não são visíveis para nós. Estão restritos apenas ao seu computador.\n\n'
            texto += '*** Opções ***\n'
            texto += 'Usar SorosGale: Ao ativar esta opção você deverá estar ciente que as entradas e gales serão de acordo com a porcentagem descrita no campo Soros e de acordo com o perfil: Conservador / Moderado / Agressivo.\n'
            texto += 'Ver o funcionamento de cada um deles através do link:\n'
            texto += '\n'
            texto += '*** Usar Pré Stop Loss ***\n'
            texto += 'Ao ativar a opção Pré Stop Loss numa situação em que você esteja perto da margem do Stop Loss, o robô interrompe as operações, evitando a ultrapassagem do Stop Loss estipulado.\n\n'
            texto += '*** Aguardar Resultado ***\n'
            texto += 'POR TAXAS - Temos o resultado pela taxa de fechamento, com isso temos um delay menor, mas com o risco do resultado ser diferente final IQ, porque no último segundo por acontecer de mudar a direção da vela.\n'
            texto += 'PELA RESPOSTA IQ - Temos o resultado pela resposta da IQ, com isso temos um delay maior, mas o resultado será 100% igual ao da IQ.\n\n'
            texto += '*** Delay ***\n'
            texto += 'Você poderá informar em que momento em fração de segundo entrará a sua ordem. Antecipando ou retardando a entrada.\n'
            texto += 'OBS. Essa opção será válida apenas para a primeira entrada. A partir da segunda dependerá do tempo de resposta da IQ Option.\n\n'
            texto += '*** Notícias ***\n'
            texto += 'Nesta, o robô filtrará as suas entradas livrando-as das notícias de 3 touros listadas no Investing.com\n'
            texto += ' Você também terá controle de quanto tempo antes e depois da notícia o robô voltará a operar.\n\n'
            texto += '*** Opções de Entradas ***\n'
            texto += 'Saldo Inicial: Valor atual da sua corretora ou um valor em que deseja trabalhar as suas operações.\n'
            texto += 'Payout Mínimo (%): Qual mínimo aceitável para realizar as operações.\n'
            texto += 'Qtd de Gale: Quantos Gales deseja realizar em suas operações\n'
            texto += 'Tipo de Stop Loss:\n'
            texto += '- Percentual: Os números dos campos de Stop Loss e Take Profit serão uma multiplicação em porcentagem vezes o valor inserido no campo Valor Inicial.\n'
            texto += '- Valor: Os números dos campos Stop Loss e Take Profit serão fixo independentemente do valor inserido no campo Valor Inicial.\n\n'
            texto += '*** Entradas Fixas ***\n'
            texto += 'Tipo:\n'
            texto += '- Percentual: Os valores dos campos de Entrada 1, Gale 1, Gale 2 serão uma multiplicação em porcentagem vezes o valor inserido no campo Valor\n'
            texto += '- Valor: Os valores dos campos de Entrada 1, Gale 1, Gale 2 serão fixos independentemente do valor inserido no campo Valor Inicial.\n\n'
            texto += '*** Botão Gravar ***\n'
            texto += 'As informações inseridas e/ou ajustadas deverão ser obrigatoriamente salvas ao clicar no Botão GRAVAR.\n\n'
            texto += '*** Fechar ***\n'
            texto += 'Para fechar as operações e o robô de entrada, o botão FECHAR localizado no canto inferior direito deverá ser acionado\n'
        return texto