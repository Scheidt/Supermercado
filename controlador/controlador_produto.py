from dao.produto_dao import ProdutoDAO
from entidade.item_carrinho import ItemCarrinho
from entidade.produto import Produto
from limite.tela_produto import TelaProduto


class ControladorProduto:
    def __init__(self, controlador_sistema, dao=None, tela=None):
        # dao e tela são injetáveis para os testes poderem rodar sem interface
        # gráfica e sem escrever na base de verdade.
        self.__controlador_sistema = controlador_sistema
        self.__dao = dao if dao is not None else ProdutoDAO()
        self.__tela = tela if tela is not None else TelaProduto()

    def abre_tela(self):
        acoes = {
            1: self.incluir_produto,
            2: self.alterar_produto,
            3: self.listar_produtos,
            4: self.excluir_produto,
            5: self.estocar,
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 0:
                return
            acoes[opcao]()

    # --- consultas ----------------------------------------------------------

    def pega_produto(self, produto_id: int):
        return self.__dao.get(produto_id)

    def listar_produtos(self, incluir_esgotados: bool = True):
        produtos = sorted(self.__dao.get_all(), key=lambda p: p.id)
        if not incluir_esgotados:
            produtos = [p for p in produtos if not p.esgotado]
        self.__tela.lista_produtos(
            [
                {
                    "id": p.id,
                    "nome": p.nome,
                    "preco": p.preco,
                    "unidade": p.unidade.value,
                    "estoque": p.estoque,
                }
                for p in produtos
            ]
        )

    # --- cadastro -----------------------------------------------------------

    def incluir_produto(self):
        dados = self.__tela.entrar_dados_produto()
        if dados is None:
            return

        existente = self.__dao.pega_por_nome(dados["nome"])
        if existente is not None:
            if dados["estoque"] > 0:
                existente.repor(dados["estoque"])
                self.__dao.update(existente)
            self.__tela.mostra_mensagem(
                f"Já existe o produto '{existente.nome}' (id {existente.id}). "
                f"O estoque informado foi somado ao dele: agora são "
                f"{existente.estoque:g} {existente.unidade}."
            )
            return

        produto = Produto(
            id=self.__dao.reserva_id(),
            nome=dados["nome"],
            preco=dados["preco"],
            unidade=dados["unidade"],
            estoque=dados["estoque"],
        )
        self.__dao.add(produto)
        self.__tela.mostra_mensagem(f"Produto '{produto.nome}' registrado com o id {produto.id}.")

    def alterar_produto(self):
        #Altera o produto no lugar.
        self.listar_produtos()
        produto = self._seleciona_produto("Alterar produto")
        if produto is None:
            return

        dados = self.__tela.alterar_dados_produto(
            {"nome": produto.nome, "preco": produto.preco, "unidade": produto.unidade.value}
        )
        if dados is None:
            return

        homonimo = self.__dao.pega_por_nome(dados["nome"])
        if homonimo is not None and homonimo.id != produto.id:
            self.__tela.mostra_erro(
                f"Já existe outro produto chamado '{homonimo.nome}' (id {homonimo.id})."
            )
            return

        produto.nome = dados["nome"]
        produto.preco = dados["preco"]
        produto.unidade = dados["unidade"]
        self.__dao.update(produto)
        self.__tela.mostra_mensagem(f"Produto '{produto.nome}' alterado com sucesso!")

    def excluir_produto(self):
        self.listar_produtos()
        produto = self._seleciona_produto("Excluir produto")
        if produto is None:
            return
        # Excluir um produto que está em algum carrinho deixaria a devolução
        # sem para onde devolver o estoque.
        if self.__controlador_sistema.controlador_carrinho.produto_em_uso(produto.id):
            self.__tela.mostra_erro(
                f"'{produto.nome}' está em algum carrinho aberto e não pode ser excluído agora."
            )
            return

        self.__dao.remove(produto.id)
        self.__tela.mostra_mensagem(f"Produto '{produto.nome}' excluído com sucesso!")

    def estocar(self):
        self.listar_produtos()
        produto = self._seleciona_produto("Estocar produto")
        if produto is None:
            return
        quantidade = self.__tela.interacao_estoque("estocar", produto.nome, produto.unidade)
        if quantidade is None:
            return
        try:
            produto.repor(quantidade)
        except ValueError as erro:
            self.__tela.mostra_erro(str(erro))
            return
        self.__dao.update(produto)
        self.__tela.mostra_mensagem(
            f"Estoque de '{produto.nome}' agora é {produto.estoque:g} {produto.unidade}."
        )

    # --- usado pelo controlador de carrinho ---------------------------------

    def retirar_para_carrinho(self):
        # Escolhe um produto, desconta do estoque e devolve o ItemCarrinho.
        # Devolve None se o usuário desistir ou se não houver o que levar.
        
        self.listar_produtos(incluir_esgotados=False)
        produto = self._seleciona_produto("Comprar produto")
        if produto is None:
            return None
        if produto.esgotado:
            self.__tela.mostra_erro(f"'{produto.nome}' está esgotado.")
            return None

        quantidade = self.__tela.interacao_estoque("comprar", produto.nome, produto.unidade)
        if quantidade is None:
            return None

        try:
            retirada = produto.retirar(quantidade)
        except ValueError as erro:
            self.__tela.mostra_erro(str(erro))
            return None

        self.__dao.update(produto)
        if retirada < quantidade:
            self.__tela.mostra_mensagem(
                f"Não havia estoque suficiente. Foram levados {retirada:g} {produto.unidade}."
            )
        if retirada <= 0:
            return None
        return ItemCarrinho.de_produto(produto, retirada)

    def devolver_do_carrinho(self, item: ItemCarrinho):
        # Repõe no estoque o item que saiu de um carrinho.
        produto = self.__dao.get(item.produto_id)
        if produto is None:
            raise LookupError(f"O produto de id {item.produto_id} não está mais no catálogo.")
        produto.repor(item.quantidade)
        self.__dao.update(produto)
        return produto

    # --- apoio --------------------------------------------------------------

    def _seleciona_produto(self, titulo: str):
        # Pede um id até achar um produto ou o usuário desistir.
        while True:
            produto_id = self.__tela.pega_id(titulo)
            if produto_id is None:
                return None
            produto = self.__dao.get(produto_id)
            if produto is not None:
                return produto
            self.__tela.mostra_erro(f"Não há produto com o id {produto_id}.")
