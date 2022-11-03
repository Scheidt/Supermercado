from limite.telaAbstrata import TelaAbstrata

class TelaSistema (TelaAbstrata):
    def __init__(self):
        super().__init__()

    

    def tela_opcoes(self):
        print("\n"*10)
        print("Supermercados P&P")
        print("Selecione a opção desejada:")
        print("1 - Produtos")
        print("2 - Clientes")
        print("3 - Carrinhos")
        print("0 - Finalizar Sistema")
        opcao = self.verifica_opção([1, 2, 3, 0])
        print("\n"*3)
        return opcao


