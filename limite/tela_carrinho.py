from limite.telaAbstrata import TelaAbstrata
import PySimpleGUI as sg


class TelaCarrinho(TelaAbstrata):
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
            [sg.Text('-------- DADOS CARRINHO ----------', font=("Helvica", 25))],
            [sg.Text('Insira o CPF do cliente', font=("Helvica", 25))],
            [sg.Text('Cpf:', size=(15, 1)), sg.InputText('', key='cpf')],                      
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Mercados P&P').Layout(layout)
        button, values = self.open()
        self.close()
        cpf = values['cpf']
        if self.verificarInt(cpf) == False:
            sg.popup("A opção escolhida deve ser um número inteiro, por favor, tente novamente: ")
        return int(cpf)

    def pega_quantidade(self, acao: str):
        print ("(Lembrando que se o produto for unitário, a quantidade inserida será arredondada para um número inteiro)")
        print("\n*3")
        print (f"Quanto de produto você deseja {acao}?")
        quantidade = input("Insira a quantia de produto desejado: ")
        while self.verificarFloat(quantidade) == False:
            quantidade = input("A quantia deve ser um valor numérico, por favor, insira novamente: ")
        return float(quantidade)

    # Recebe uma lista de dicionários no formato: [
    # {'cliente': Cliente, 'produto': [produto, produto,...]}
    # {'cliente': Cliente, 'produto': [produto, produto,...]}
    # {'cliente': Cliente, 'produto': [produto, produto,...]}
    # ...]
    def listar_carrinhos(self, lista_de_carrinhos: list):
        string_todos_carrinhos = ""
        if lista_de_carrinhos is not None:
            for dados in lista_de_carrinhos:
                string_todos_carrinhos = string_todos_carrinhos +  f"Dados do(a) cliente:" + '\n'
                string_todos_carrinhos = string_todos_carrinhos + f"  Nome: {dados['nome']}" + '\n'
                string_todos_carrinhos = string_todos_carrinhos + f"  CPF: {dados['cpf']}" + '\n'
                if dados['produtos'] != 0:
                    string_todos_carrinhos = string_todos_carrinhos +  f"{'Nome':^20}{'ID':^5}   {'Preco':^7}{'Quantidade':^9}   {'Subtotal':^9}" + '\n'
                    for produto in dados['produtos']:
                        string_todos_carrinhos = string_todos_carrinhos + f"\
{produto['nome']:^20}\
{produto['id']:^5}   \
{produto['preco']:^7}\
{produto['quantidade']:^9}   \
{produto['subtotal']:^8,.2f}" + '\n'
                    string_todos_carrinhos = string_todos_carrinhos + f"Total: {dados['total']}" + '\n'
                else:
                    string_todos_carrinhos = string_todos_carrinhos + "    Este carrinho está vazio, adicione alguns produtos!" + '\n'
                string_todos_carrinhos = string_todos_carrinhos + "\n"*2
        else:
            string_todos_carrinhos = string_todos_carrinhos + "Não há nenhum carrinho registrado. Por favor, registre algum carrinho." + '\n'
        sg.popup_annoying('LISTA DE CARRINHOS', string_todos_carrinhos)


    def mostra_cliente(self, dados: dict):
        print(f"Dados do(a) cliente:")
        print(f"  Nome: {dados['nome']}")
        print(f"  CPF: {dados['cpf']}")

    def mostra_carrinho(self, cliente: dict, compras: dict, total: float):
        print(f"Cliente: {cliente['nome']}")
        print(f"CPF: {cliente['cpf']}")
        if len(compras) != 0:
            print(f"{'Nome':^20}{'ID':^5}   {'Preco':^7}{'Quantidade':^9}   {'Subtotal':^9}")
            for produto in compras:
                print(f"\
{produto['nome']:^20}\
{produto['id']:^5}   \
{produto['preco']:^7}\
{produto['quantidade']:^9}   \
{produto['subtotal']:^8,.2f}")
            print(f"Total = {total}")
        else:
            self.mostra_mensagem("Este carrinho está vazio, adicione alguns produtos!")

    def pega_id_produto(self):
        id = input("Insira a id do produto: ")
        while self.verificarInt(id) == False:
                id = input("A opção escolhida deve ser um número inteiro, por favor, tente novamente: ")
        return int(id)

    def init_components(self):
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
            [sg.Text('Carrinhos', font=("Helvica",25))],
            [sg.Text('Escolha sua opção: ', font=("Helvica",15))],
            [sg.Radio('Criar um novo carrinho',"RD1", key='1')],
            [sg.Radio('Comprar um produto',"RD1", key='2')],
            [sg.Radio('Devolver um Produto',"RD1", key='3')],
            [sg.Radio('Listar carrinhos',"RD1", key='4')],
            [sg.Radio('Finalizar carrinho',"RD1", key='5')],
            [sg.Radio('Retonar',"RD1", key='0')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]

        ]
        self.__window = sg.Window('Mercado P&P').Layout(layout)
      
    def open(self):
        button, values = self.__window.Read()
        return button, values

