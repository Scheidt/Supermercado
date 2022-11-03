from limite.tela_sistema import TelaSistema
from controlador.controlador_produto import ControladorProduto
from controlador.controlador_cliente import ControladorCliente
from controlador.controlador_carrinho import ControladorCarrinho

class ControladorSistema:

    def __init__(self):
        self.__controlador_produto = ControladorProduto(self)
        self.__controlador_cliente = ControladorCliente(self)
        self.__controlador_carrinho = ControladorCarrinho(self)
        self.__tela_sistema = TelaSistema()

    @property
    def controlador_produto(self):
        return self.__controlador_produto

    @property
    def controlador_cliente(self):
        return self.__controlador_cliente
    
    @property
    def controlador_carrinho(self):
        return self.__controlador_carrinho

    def inicializa_sistema(self):
        self.abre_tela()

    def menu_produto(self):
        self.__controlador_produto.menu()

    def menu_cliente(self):
        self.__controlador_cliente.menu()

    def menu_carrinho(self):
        self.__controlador_carrinho.menu()

    def encerra_sistema(self):
        exit(4)

    def abre_tela(self):
        lista_opcoes = {1: self.menu_produto,
                        2: self.menu_cliente,
                        3: self.menu_carrinho,
                        4: self.encerra_sistema}

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()
