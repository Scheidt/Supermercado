from dao.carrinho_dao import CarrinhoDAO
from entidade import cpf as cpf_util
from entidade.carrinho import Carrinho
from limite.tela_carrinho import TelaCarrinho


class ControladorCarrinho:
    def __init__(self, controlador_sistema, dao=None, tela=None):
        self.__controlador_sistema = controlador_sistema
        self.__dao = dao if dao is not None else CarrinhoDAO()
        self.__tela = tela if tela is not None else TelaCarrinho()

    def abre_tela(self):
        acoes = {
            1: self.incluir_carrinho,
            2: self.comprar,
            3: self.devolver,
            4: self.listar_carrinhos,
            5: self.finalizar_carrinho,
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 0:
                return
            acoes[opcao]()

    # --- consultas usadas pelos outros controladores ------------------------

    def cliente_tem_carrinho(self, cpf: str) -> bool:
        return cpf in self.__dao

    def produto_em_uso(self, produto_id: int) -> bool:
        return any(c.item(produto_id) is not None for c in self.__dao.get_all())

    # --- operações ----------------------------------------------------------

    def incluir_carrinho(self):
        self.__controlador_sistema.controlador_cliente.listar_clientes()
        while True:
            cpf = self.__tela.pega_cpf("Criar carrinho")
            if cpf is None:
                return
            cliente = self.__controlador_sistema.controlador_cliente.pega_cliente(cpf)
            if cliente is None:
                self.__tela.mostra_erro(f"Não há cliente com o CPF {cpf_util.formata(cpf)}.")
                continue
            if self.cliente_tem_carrinho(cpf):
                self.__tela.mostra_erro(f"{cliente.nome} já possui um carrinho aberto.")
                continue
            self.__dao.add(Carrinho(cpf))
            self.__tela.mostra_mensagem(f"Carrinho de {cliente.nome} registrado com sucesso!")
            return

    def comprar(self):
        self.listar_carrinhos()
        carrinho = self._seleciona_carrinho("Comprar produto")
        if carrinho is None:
            return
        item = self.__controlador_sistema.controlador_produto.retirar_para_carrinho()
        if item is None:
            return
        carrinho.adicionar(item)
        self.__dao.update(carrinho)
        self.__tela.mostra_mensagem(
            f"{item.quantidade:g} {item.unidade} de '{item.nome}' no carrinho."
        )

    def devolver(self):
        self.listar_carrinhos()
        carrinho = self._seleciona_carrinho("Devolver produto")
        if carrinho is None:
            return
        if carrinho.vazio:
            self.__tela.mostra_erro("Este carrinho está vazio, não há o que devolver.")
            return

        self.__tela.mostra_carrinho(self._dados(carrinho))
        produto_id = self.__tela.pega_id_produto()
        if produto_id is None:
            return

        try:
            item = carrinho.remover(produto_id)
        except KeyError:
            self.__tela.mostra_erro(f"Não há produto com o id {produto_id} neste carrinho.")
            return

        try:
            self.__controlador_sistema.controlador_produto.devolver_do_carrinho(item)
        except (LookupError, ValueError) as erro:
            # Devolve o item ao carrinho: melhor o item continuar lá do que
            # sumir do carrinho sem ter voltado para o estoque.
            carrinho.adicionar(item)
            self.__tela.mostra_erro(f"Não foi possível devolver o produto: {erro}")
            return

        self.__dao.update(carrinho)
        self.__tela.mostra_mensagem(f"'{item.nome}' devolvido ao estoque com sucesso!")

    def listar_carrinhos(self):
        carrinhos = self.__dao.get_all()
        self.__tela.lista_carrinhos([self._dados(c) for c in carrinhos])

    def finalizar_carrinho(self):
        # Fecha a compra: registra o gasto no cliente e apaga o carrinho.
        self.listar_carrinhos()
        carrinho = self._seleciona_carrinho("Finalizar carrinho")
        if carrinho is None:
            return
        if carrinho.vazio:
            self.__tela.mostra_erro("Este carrinho está vazio, não há o que finalizar.")
            return

        total = carrinho.total
        try:
            cliente = self.__controlador_sistema.controlador_cliente.registrar_compra(
                carrinho.cliente_cpf, total
            )
        except LookupError as erro:
            self.__tela.mostra_erro(f"Não foi possível finalizar: {erro}")
            return

        self.__dao.remove(carrinho.cliente_cpf)
        self.__tela.mostra_mensagem(
            f"Compra de {cliente.nome} finalizada: R$ {total:,.2f}."
        )

    # --- apoio --------------------------------------------------------------

    def _seleciona_carrinho(self, titulo: str):
        while True:
            cpf = self.__tela.pega_cpf(titulo)
            if cpf is None:
                return None
            carrinho = self.__dao.get(cpf)
            if carrinho is not None:
                return carrinho
            self.__tela.mostra_erro(f"Não há carrinho para o CPF {cpf_util.formata(cpf)}.")

    def _dados(self, carrinho: Carrinho) -> dict:
        cliente = self.__controlador_sistema.controlador_cliente.pega_cliente(carrinho.cliente_cpf)
        itens = []
        for item in carrinho.itens:
            dados_item = item.to_dict()
            dados_item["subtotal"] = item.subtotal
            itens.append(dados_item)
        return {
            "cliente_nome": cliente.nome if cliente else "(cliente removido)",
            "cliente_cpf": carrinho.cliente_cpf,
            "itens": itens,
            "total": carrinho.total,
        }
