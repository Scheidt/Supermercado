from entidade.cliente import Cliente
from limite.tela_cliente import TelaCliente

class ControladorCliente():
    def __init__(self, controlador_sistema) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaCliente()
        self.__clientes = []
        # nome: str, cpf: int, gasto = 0
        if False:
            self.__clientes = [Cliente("Pedro", 11, 153.5),
                            Cliente("João", 22, 153.5),
                            Cliente("William", 33, 777.00),
                            Cliente("Thaís", 44, 999.00),
                            Cliente("Dwayne Johnson", 55, 3.00)]

    def menu(self):
        """
        print("1 - Cadastrar um cliente")
        print("2 - Alterar um cliente")
        print("3 - Excluir um cliente")
        print("4 - Listar clientes")
        print("5 - Listar clientes por gasto")
        print("0 - Retornar")
        """
        switcher = {0: self.finalizar,
                    1: self.incluir_cliente,
                    2: self.alterar_cliente,
                    3: self.excluir_cliente,
                    4: self.listar_clientes,
                    5: self.pega_melhor_cliente} # FAZER
        while True:  
            opção = self.__tela.tela_opcoes()
            if opção == 0:
                break
            funcao_escolhida = switcher[opção]
            funcao_escolhida()
    
    def incluir_cliente(self):   
        dados = self.__tela.entrar_dados_cliente()
        cliente = self.pega_cliente_por_cpf(dados["cpf"])    
        if cliente == None:
            self.__clientes.append(Cliente(dados["nome"], dados["cpf"]))
            self.__tela.mostra_mensagem ("Cadastro feito!")
        else:
            self.__tela.mostra_mensagem ("Cliente já registrado!")

    def alterar_cliente(self):
        self.listar_clientes()
        cpf = self.__tela.pega_cpf()
        cliente = self.pega_cliente_por_cpf(cpf)
        while cliente is None and cpf != 0:
            self.listar_clientes()
            cpf = self.__tela.pega_cpf()
            if cpf == 0:
                break
            cliente = self.pega_cliente_por_cpf(cpf)
        if cpf != 0:
            self.__clientes.remove(cliente)
            self.incluir_cliente()
    
    def excluir_cliente(self):
        self.listar_clientes()
        cpf = self.__tela.pega_cpf()
        cliente = self.pega_cliente_por_cpf(cpf)
        if cliente == None:
            self.__tela.mostra_mensagem ("O cliente que você quer deletar não aparece no cadasto, você digitou o CPF corretamente?")
        else:
            self.__clientes.remove(cliente)
            del cliente
            self.__tela.mostra_mensagem ("Cliente deletado com sucesso!")

    def listar_clientes(self):
        for i in range(len(self.__clientes)):
            self.__tela.mostra_cliente({'num': i+1,
                                        'nome': self.__clientes[i].nome,
                                        'cpf': self.__clientes[i].cpf,
                                        'gasto': self.__clientes[i].totalcompras})

    def pega_cliente_por_cpf(self, cpf: int):
        for i in range(len(self.__clientes)):
            if self.__clientes[i].cpf == cpf:
                return self.__clientes[i]
        return None
    
    def finalizar(self):
            self.__controlador_sistema.abre_tela()

    def registrar_compra(self, pacote: dict): # Pacote no formato {'cliente': Cliente, 'gasto': float}
        cliente = self.pega_cliente_por_cpf(pacote['cliente'].cpf)
        if cliente == None:
            self.__tela.mostra_mensagem("Há um erro no registro do cliente deste carrinho, boa sorte procurando o erro!")
        indice_cliente = self.__clientes.index(cliente)
        self.__clientes[indice_cliente].comprou(pacote['gasto'])
    
    def pega_melhor_cliente(self):
        try:
            if len(self.__clientes) == 0:
                raise KeyError           
            else:
                self.__tela.mostra_mensagem("--------------------- Clientes que mais gastaram ---------------------")
                self.__tela.mostra_mensagem(f"{'Nome:':30}{'Gasto:':^10}")
                melhores = []
                totais = [] 
                par = []    
                for cliente in self.__clientes:           
                    totais.append(cliente.totalcompras)
                totais = set(totais)
                totais = list(totais)
                totais.sort(reverse = True)
                while len(melhores) != len(self.__clientes):
                    for i in range(len(totais)):
                        for cliente in self.__clientes:
                            par = []
                            if cliente.totalcompras == totais[i]:
                                par.append(cliente.nome)
                                par.append(cliente.totalcompras)
                                melhores.append(par)
                self.__tela.mostra_melhores(melhores)
        except KeyError:
            self.__tela.mostra_mensagem("Ainda não há nenhum cliente cadastrado.")
            