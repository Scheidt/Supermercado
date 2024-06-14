import PySimpleGUI as sg
from limite.telaAbstrata import TelaAbstrata


class TelaCliente(TelaAbstrata):
      def __init__(self):
            super().__init__()

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
        if values['4']:
            opcao = 4
        if values['5']:
            opcao = 5       
        if values['0'] or button in (None,'Cancelar'):
            opcao = 0
        self.close()
        return opcao
    
      def close(self):
            self.__window.Close()

      def pega_cpf(self):
            sg.ChangeLookAndFeel('DarkTeal4')
            layout = [
                  [sg.Text('-------- SELECIONAR CLIENTE ----------', font=("Helvica", 25))],
                  [sg.Text('Digite o CPF do cliente que deseja selecionar:', font=("Helvica", 15))],
                  [sg.Text('CPF:', size=(15, 1)), sg.InputText('', key='cpf')],
                  [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
            ]
            self.__window = sg.Window('Seleciona Cliente').Layout(layout)                                     
            button, values = self.open()
            self.close()
            cpf = values['cpf']
            if self.verificarInt(cpf) == False:
                  sg.popup_annoying("Digite somente valores inteiros")
            else:      
                  cpf = int(values['cpf'])
                  return cpf

      def entrar_dados_cliente(self):
            sg.ChangeLookAndFeel('DarkTeal4')
            layout = [
            [sg.Text('-------- DADOS CLIENTE ----------', font=("Helvica", 25))],
            [sg.Text('Nome:', size=(15, 1)), sg.InputText('', key='nome')],
            [sg.Text('CPF:', size=(15, 1)), sg.InputText('', key='cpf')],            
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
            ]
            self.__window = sg.Window('Mercados P&P').Layout(layout)

            button, values = self.open()
            nome = values['nome']
            cpf = values['cpf']
            if self.verificarString(nome) == False:
                  sg.popup_annoying("Digite somente letras")
            if self.verificarInt(cpf) == False:
                  sg.popup_annoying("Digite somente números inteiros")
            self.close()
            cpf = int(cpf)
            return {"nome": nome, "cpf": cpf}

      def mostra_cliente(self, dados_clientes):
         
            string_todos_clientes = ""
            for dado in dados_clientes:
                  string_todos_clientes = string_todos_clientes + "NOME DO CLIENTE: " + str(dado["nome"]) + '\n'
                  string_todos_clientes = string_todos_clientes + "CPF DO CLIENTE: " + str(dado["cpf"]) + '\n'
                  string_todos_clientes = string_todos_clientes + "TOTAL GASTO: " + str(dado["gasto"]) + '\n\n'

            sg.popup_annoying('-------- LISTA DE CLIENTES ----------', string_todos_clientes)
           
            

      def mostra_melhores(self, dados_melhores: list):
            string_melhores = f"{'Nome:':30}{'Gasto:':^10}\n"
            for i in range(len(dados_melhores)):
                  string_melhores = string_melhores + f"{dados_melhores[i][0]:30}" + f"{dados_melhores[i][1]:^10,.2f}\n"                  

            sg.popup_annoying("LISTA DOS MELHORES CLIENTES", string_melhores)

      def init_components(self):
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
            [sg.Text('Clientes', font=("Helvica",25))],
            [sg.Text('Escolha sua opção: ', font=("Helvica",15))],
            [sg.Radio('Cadastrar um cliente',"RD1", key='1')],
            [sg.Radio('Alterar um cliente',"RD1", key='2')],
            [sg.Radio('Excluir um cliente',"RD1", key='3')],
            [sg.Radio('Listar clientes',"RD1", key='4')],
            [sg.Radio('Listar clientes por gasto',"RD1", key='5')],
            [sg.Radio('Retonar',"RD1", key='0')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]

        ]
        self.__window = sg.Window('Mercado P&P').Layout(layout)
      
      def open(self):
            button, values = self.__window.Read()
            return button, values

      
      
            
