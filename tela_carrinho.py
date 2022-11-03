from limite.telaAbstrata import TelaAbstrata


class TelaCarrinho(TelaAbstrata):
    def __init__(self):
        super().__init__()

    def tela_opcoes(self):
        print("-------- Opções Carrinho ----------")
        print("1 - Criar novo carrinho")
        print("2 - Comprar um produto")
        print("3 - Devolver um produto")
        print("4 - Listar carrinhos")
        print("5 - Finalizar um carrinho")
        print("0 - Retornar")

        opcao = self.verifica_opção((0, 1, 2, 3, 4, 5))
        print("\n"*3)
        return opcao

    def pega_cpf(self):
        cpf = input("Insira o CPF do cliente: ")
        while self.verificarInt(cpf) == False:
            cpf = input("A opção escolhida deve ser um número inteiro, por favor, tente novamente: ")
        return int(cpf)

    def pega_quantidade(self, acao: str):
        print ("(Lembrando que se o produto for unitário, a quantidade inserida será arredondada para um número inteiro)")
        print("\n*3")
        print (f"Quanto de produto você deseja {acao}?")
        quantidade = input("Insira a quantia de produto desejado: ")
        while self.verificarFloat(quantidade) == False:
            quantidade = input("A quantia deve ser um valor numérico, por favor, insira novamente: ")
        return float(quantidade)

    def mostra_carrinho(self, dados: dict):
        print(f"Dados do(a) cliente:")
        print(f"  Nome: {dados['nome']}")
        print(f"  CPF: {dados['cpf']}")

    def listar(self, dados: dict):
        print(f"\
{dados['nome']:^20}\
{dados['id']:^5}   \
{dados['preco']:^7}\
{dados['quantidade']:^9}   \
{dados['subtotal']:^8,.2f}")

    def pega_id_produto(self):
        id = input("Insira a id do produto: ")
        while self.verificarInt(id) == False:
                id = input("A opção escolhida deve ser um número inteiro, por favor, tente novamente: ")
        return int(id)

