import PySimpleGUI as sg
from limite.telaAbstrata import TelaAbstrata

class TelaSistema (TelaAbstrata):
    def __init__(self):
        super().__init__()
        self.init_components()   

    def tela_opcoes(self):
        self.init_components()
        button, values = self.__window.Read()
        opcao = 0
        if values['1']:
            opcao = 1
        if values['2']:
            opcao = 2
        if values['3']:
            opcao = 3       
        if values['0'] or button in (None,'Cancelar'):
            opcao = 0
        self.close()
        return opcao
    
    def close(self):
        self.__window.Close()

    def init_components(self):
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
            [sg.Text('Bem vindo ao mercado P&P!', font=("Helvica",25))],
            [sg.Text('Escolha sua opção: ', font=("Helvica",15))],
            [sg.Radio('Produtos',"RD1", key='1')],
            [sg.Radio('Clientes',"RD1", key='2')],
            [sg.Radio('Carrinhos',"RD1", key='3')],
            [sg.Radio('Finalizar Sistema',"RD1", key='0')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Mercado P&P').Layout(layout)


