import PySimpleGUI as sg
from limite.telaAbstrata import TelaAbstrata


class TelaProduto (TelaAbstrata):
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

    def pega_id(self):
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
                [sg.Text('-------- SELECIONAR PRODUTO ----------', font=("Helvica", 25))],
                [sg.Text('Digite o ID do produto que deseja selecionar:', font=("Helvica", 15))],
                [sg.Text('ID:', size=(15, 1)), sg.InputText('', key='id')],
                [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Seleciona Produto').Layout(layout)  
        button, values = self.open()
        self.close()
        id = values['id']
        if self.verificarInt(id) == False:
                sg.popup_annoying("Digite somente valores inteiros")
        else:      
                id = int(values['id'])
                return id
    
    def entrar_dados_produto(self):
        validado = 0
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
            [sg.Text('-------- DADOS PRODUTOS ----------', font=("Helvica", 25))],
            [sg.Text('Nome:', size=(15, 1)), sg.InputText('', key='nome')],
            [sg.Text('Preço:', size=(15, 1)), sg.InputText('', key='preco')], 
            [sg.Text('Unidade:', size=(15, 1)), sg.InputText('', key='unidade')],   
            [sg.Text('Estoque:', size=(15, 1)), sg.InputText('', key='estoque')],        
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Mercados P&P').Layout(layout)
        button, values = self.open()
        nome = values['nome']
        preco = values['preco']
        unidade = values['unidade']
        estoque = values['estoque']
        if self.verificarString(nome) == False:
            sg.popup("Insira apenas letras")
            validado += 1
        if self.verificarFloat(preco) == False:
            sg.popup("Preço deve ser um valor numérico, por favor, insira novamente")           
            validado += 1
        if self.verificarString(unidade) == False:
            sg.popup("Valor deve ser uma opção como Kg, litro ou Unidade")
            validado += 1
        if self.verificarFloat(estoque) == False:
            sg.popup("Estoque deve ser um valor numérico, por favor, insira novamente")       
            validado += 1
        self.close()
        if validado == 0:
            preco = float(preco)
            estoque = float(estoque)
            return {"nome": nome, "preco": preco, "unidade": unidade, "estoque": estoque}

    def listar_produtos(self, dados: list):
        string_final = f"------------------- Informações dos Produtos Registrados -------------------\n"
        if dados is not None:
            string_final = string_final + f"{'Nome: ':20}{'Id: ':^5}   {'Preço: ':^7}{'Unidade: ':^18}{'Quantidade: ':^9} " + '\n'
            for produto in dados:
                string_final = string_final + (f"\
{produto['nome']:20}\
{produto['id']:^5}   \
{produto['preco']:^7,.2f}\
{produto['unidade']:^18}\
{produto['estoque']:^9}\n")
        else:
            string_final = string_final + "Nenhum produto foi registrado. Por favor, registre algum produto!"
        sg.popup_annoying("LISTA DE PRODUTOS", string_final)

    def interacao_estoque(self, acao: str, nome: str):
        self.mostra_mensagem("(Lembrando que se o produto for unitário, a quantidade inserida será arredondada para um número inteiro)")
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
            [sg.Text(f'-------- {acao} ----------', font=("Helvica", 25))],
            [sg.Text(f'Insira a quantidade de {nome}', font=("Helvica", 25))],
            [sg.Text('Quantidade:', size=(15, 1)), sg.InputText('', key='quantidade')],                      
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Mercados P&P').Layout(layout)
        button, values = self.open()
        self.close()
        quantidade = values['quantidade']
        if self.verificarFloat(quantidade) == False:
            sg.popup("A quantia deve ser um valor numérico, por favor, insira novamente: ")
        return float(quantidade)

    def init_components(self):
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
            [sg.Text('Produtos', font=("Helvica",25))],
            [sg.Text('Escolha sua opção: ', font=("Helvica",15))],
            [sg.Radio('Incluir Produto',"RD1", key='1')],
            [sg.Radio('Alterar um Produto',"RD1", key='2')],
             [sg.Radio('Listar Produtos',"RD1", key='3')],
            [sg.Radio('Excluir um Produto',"RD1", key='4')],
            [sg.Radio('Estocar Produtos', "RD1", key='5')],
            [sg.Radio('Retonar',"RD1", key='0')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Mercado P&P').Layout(layout)

    def open(self):
            button, values = self.__window.Read()
            return button, values