from limite.telaAbstrata import TelaAbstrata


class TelaProduto (TelaAbstrata):
    def __init__(self):
        super().__init__()

    def tela_opcoes(self):
        print("-------- Opções Produto ----------")
        print("Escolha a opcao")
        print("1 - Incluir Produto")
        print("2 - Alterar Produto")
        print("3 - Listar Produtos")
        print("4 - Excluir Produto")
        print("5 - Reordenar IDs")
        print("6 - Estocar Produtos")
        print("0 - Voltar")

        opcao = self.verifica_opção((0, 1, 2, 3, 4, 5, 6))
        print("\n"*3)
        return opcao

    def pega_id(self):
        id = input("Insira a ID do produto desejado: ")
        while self.verificarInt(id) == False:
            id = input("A opção escolhida deve ser um número inteiro, por favor, tente novamente: ")
        return int(id)
    
    def entrar_dados_produto(self):
        print("-------- Insira os dados do produto ----------")
        # Setar nome
        nome = input("Nome: ")
        while self.verificarString(nome) == False:
            nome = input("Nome: ")
        # Setar preço
        preco = input("Preço: ")
        while self.verificarFloat(preco) == False:
            preco = input("Preço deve ser um valor numérico, por favor, insira novamente: ")
        preco = float(preco)
        # Setar unidade de medida
        unidade = input("Unidade de medida (Ex.: Unidade, Kg): ")
        while self.verificarString == False:
            unidade = input("Unidade de medida (Ex.: Unidade, Kg): ")
        # Setar estoque
        estoque = input("Estoque: ")
        while self.verificarFloat(estoque) == False:
            estoque = input("Estoque deve ser um valor numérico, por favor, insira novamente: ")
        estoque = float(estoque)
        return {"nome": nome, "preco": preco, "unidade": unidade, "estoque": estoque}

    def listar(self, dados: dict):
        print(f"\
{dados['nome']:20}\
{dados['id']:^5}   \
{dados['preco']:^7,.2f}\
{dados['unidade']:^18}\
{dados['estoque']:^9}")

    def interacao_estoque(self, acao: str, nome: str):
        print("\n"*3)
        print ("(Lembrando que se o produto for unitário, a quantidade inserida será arredondada para um número inteiro)")
        quantidade = input(f"Insira a quantidade de {nome} que deseja {acao}: ")
        while self.verificarFloat(quantidade) == False:
            quantidade = input("A quantia deve ser um valor numérico, por favor, insira novamente: ")
        return float(quantidade)