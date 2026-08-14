from dao.abstract_dao import ChaveDuplicadaError
from dao.cliente_dao import ClienteDAO
from entidade import cpf as cpf_util
from entidade.cliente import Cliente
from limite.tela_cliente import TelaCliente


class ControladorCliente:
    def __init__(self, controlador_sistema, dao=None, tela=None):
        self.__controlador_sistema = controlador_sistema
        self.__dao = dao if dao is not None else ClienteDAO()
        self.__tela = tela if tela is not None else TelaCliente()

    def abre_tela(self):
        acoes = {
            1: self.incluir_cliente,
            2: self.alterar_cliente,
            3: self.excluir_cliente,
            4: self.listar_clientes,
            5: self.listar_por_gasto,
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 0:
                return
            acoes[opcao]()

    # --- consultas ----------------------------------------------------------

    def pega_cliente(self, cpf: str):
        return self.__dao.get(cpf)

    def listar_clientes(self):
        clientes = sorted(self.__dao.get_all(), key=lambda c: c.nome.casefold())
        self.__tela.lista_clientes([self._dados(c) for c in clientes])

    def listar_por_gasto(self):
        #Clientes do maior para o menor gasto.
        clientes = sorted(self.__dao.get_all(), key=lambda c: c.total_compras, reverse=True)
        self.__tela.lista_melhores([self._dados(c) for c in clientes])

    # --- cadastro -----------------------------------------------------------

    def incluir_cliente(self):
        dados = self.__tela.entrar_dados_cliente()
        if dados is None:
            return
        try:
            self.__dao.add(Cliente(cpf=dados["cpf"], nome=dados["nome"]))
        except ChaveDuplicadaError:
            self.__tela.mostra_erro(
                f"O CPF {cpf_util.formata(dados['cpf'])} já está cadastrado."
            )
            return
        self.__tela.mostra_mensagem(f"Cliente '{dados['nome']}' cadastrado com sucesso!")

    def alterar_cliente(self):
        # Altera o nome do cliente no lugar.
        self.listar_clientes()
        cliente = self._seleciona_cliente("Alterar cliente")
        if cliente is None:
            return
        nome = self.__tela.altera_nome(cliente.nome)
        if nome is None:
            return
        cliente.nome = nome
        self.__dao.update(cliente)
        self.__tela.mostra_mensagem("Cliente alterado com sucesso!")

    def excluir_cliente(self):
        self.listar_clientes()
        cliente = self._seleciona_cliente("Excluir cliente")
        if cliente is None:
            return
        if self.__controlador_sistema.controlador_carrinho.cliente_tem_carrinho(cliente.cpf):
            self.__tela.mostra_erro(
                f"'{cliente.nome}' tem um carrinho aberto. Finalize ou esvazie o carrinho antes."
            )
            return
        self.__dao.remove(cliente.cpf)
        self.__tela.mostra_mensagem(f"Cliente '{cliente.nome}' excluído com sucesso!")

    # --- usado pelo controlador de carrinho ---------------------------------

    def registrar_compra(self, cpf: str, valor: float):
        # Soma o valor da compra ao total gasto do cliente e grava.
        # Levanta LookupError se o cliente não existir.
        cliente = self.__dao.get(cpf)
        if cliente is None:
            raise LookupError(f"Não há cliente com o CPF {cpf}.")
        cliente.registrar_compra(valor)
        self.__dao.update(cliente)
        return cliente

    # --- apoio --------------------------------------------------------------

    def _seleciona_cliente(self, titulo: str):
        while True:
            cpf = self.__tela.pega_cpf(titulo)
            if cpf is None:
                return None
            cliente = self.__dao.get(cpf)
            if cliente is not None:
                return cliente
            self.__tela.mostra_erro(f"Não há cliente com o CPF {cpf_util.formata(cpf)}.")

    @staticmethod
    def _dados(cliente: Cliente) -> dict:
        return {
            "cpf": cliente.cpf_formatado,
            "nome": cliente.nome,
            "total_compras": cliente.total_compras,
        }
