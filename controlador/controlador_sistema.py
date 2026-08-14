from controlador.controlador_carrinho import ControladorCarrinho
from controlador.controlador_cliente import ControladorCliente
from controlador.controlador_produto import ControladorProduto
from limite.tela_sistema import TelaSistema


class ControladorSistema:
    def __init__(self):
        self.__tela = TelaSistema()
        self.__controlador_produto = ControladorProduto(self)
        self.__controlador_cliente = ControladorCliente(self)
        self.__controlador_carrinho = ControladorCarrinho(self)

    @property
    def controlador_produto(self) -> ControladorProduto:
        return self.__controlador_produto

    @property
    def controlador_cliente(self) -> ControladorCliente:
        return self.__controlador_cliente

    @property
    def controlador_carrinho(self) -> ControladorCarrinho:
        return self.__controlador_carrinho

    def inicializa_sistema(self):
        acoes = {
            1: self.__controlador_produto.abre_tela,
            2: self.__controlador_cliente.abre_tela,
            3: self.__controlador_carrinho.abre_tela,
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 0:
                self.__tela.mostra_mensagem("Até logo!")
                return
            acoes[opcao]()
