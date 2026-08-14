import FreeSimpleGUI as sg

from entidade.unidade import Unidade
from limite.tela_abstrata import TelaAbstrata, FONTE_TITULO, LARGURA_CAMPO, LARGURA_ROTULO

OPCOES = {
    1: "Incluir produto",
    2: "Alterar um produto",
    3: "Listar produtos",
    4: "Excluir um produto",
    5: "Estocar produtos",
    0: "Retornar",
}

_UNIDADES = [u.value for u in Unidade]


class TelaProduto(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._menu("Mercado P&P", "Produtos", OPCOES)

    def pega_id(self, titulo: str = "Selecionar produto"):
        """Devolve o id do produto, ou None se cancelar ou digitar errado."""
        valores = self._formulario(titulo, titulo, [("id", "ID:")])
        if valores is None:
            return None
        return self._para_inteiro(valores["id"], "O ID")

    def entrar_dados_produto(self):
        """Dados de um produto novo, ou None se cancelar ou preencher errado."""
        dados = self._formulario_produto("Cadastro de produto", pedir_estoque=True)
        return dados

    def alterar_dados_produto(self, produto_atual: dict):
        """Edita nome, preço e unidade de um produto existente.

        O estoque não entra aqui: ele muda por "Estocar", por compra e por
        devolução. A tela vem preenchida com os valores atuais, então alterar um
        campo não obriga a redigitar os outros.
        """
        return self._formulario_produto(
            "Alterar produto", pedir_estoque=False, valores_iniciais=produto_atual
        )

    def interacao_estoque(self, acao: str, produto_nome: str, unidade: Unidade):
        """Pede uma quantidade. Devolve float, ou None se cancelar/errar."""
        aviso = (
            "Produto vendido por unidade: a quantidade será arredondada."
            if not unidade.fracionavel
            else f"Quantidade em {unidade.value}."
        )
        layout = [
            [sg.Text(acao.capitalize(), font=FONTE_TITULO)],
            [sg.Text(f"Produto: {produto_nome}")],
            [sg.Text(aviso)],
            [sg.Text("Quantidade:", size=LARGURA_ROTULO), sg.InputText("", key="quantidade", size=LARGURA_CAMPO)],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")],
        ]
        evento, valores = self._abre("Mercado P&P", layout)
        if self._cancelou(evento, valores):
            return None
        quantidade = self._para_decimal(valores["quantidade"], "A quantidade")
        if quantidade is None:
            return None
        if quantidade <= 0:
            self.mostra_erro("A quantidade deve ser maior que zero.")
            return None
        return quantidade

    def lista_produtos(self, produtos: list):
        if not produtos:
            self.mostra_mensagem("Nenhum produto cadastrado ainda.")
            return
        linhas = [f"{'ID':<5}{'Nome':<28}{'Preço':>10}  {'Unidade':<12}{'Estoque':>10}", "-" * 67]
        for dados in produtos:
            linhas.append(
                f"{dados['id']:<5}{dados['nome']:<28}{dados['preco']:>10,.2f}  "
                f"{dados['unidade']:<12}{dados['estoque']:>10,.3f}"
            )
        self.mostra_tabela("Lista de produtos", "\n".join(linhas))

    def _formulario_produto(self, titulo: str, pedir_estoque: bool, valores_iniciais: dict = None):
        atuais = valores_iniciais or {}
        unidade_inicial = atuais.get("unidade", Unidade.UNIDADE.value)
        layout = [
            [sg.Text(titulo, font=FONTE_TITULO)],
            [sg.Text("Nome:", size=LARGURA_ROTULO),
             sg.InputText(atuais.get("nome", ""), key="nome", size=LARGURA_CAMPO)],
            [sg.Text("Preço:", size=LARGURA_ROTULO),
             sg.InputText(atuais.get("preco", ""), key="preco", size=LARGURA_CAMPO)],
            [sg.Text("Unidade:", size=LARGURA_ROTULO),
             sg.Combo(_UNIDADES, default_value=unidade_inicial, key="unidade",
                      size=LARGURA_CAMPO, readonly=True)],
        ]
        if pedir_estoque:
            layout.append(
                [sg.Text("Estoque:", size=LARGURA_ROTULO),
                 sg.InputText("", key="estoque", size=LARGURA_CAMPO)]
            )
        layout.append([sg.Button("Confirmar"), sg.Cancel("Cancelar")])

        evento, valores = self._abre("Mercado P&P", layout)
        if self._cancelou(evento, valores):
            return None

        nome = self._texto_obrigatorio(valores["nome"], "O nome")
        if nome is None:
            return None
        preco = self._para_decimal(valores["preco"], "O preço")
        if preco is None:
            return None
        if preco < 0:
            self.mostra_erro("O preço não pode ser negativo.")
            return None
        # O Combo é readonly, então a unidade só pode ser um dos valores válidos.
        unidade = Unidade.de_texto(valores["unidade"])

        dados = {"nome": nome, "preco": preco, "unidade": unidade}
        if pedir_estoque:
            estoque = self._para_decimal(valores["estoque"], "O estoque")
            if estoque is None:
                return None
            if estoque < 0:
                self.mostra_erro("O estoque não pode ser negativo.")
                return None
            dados["estoque"] = estoque
        return dados
