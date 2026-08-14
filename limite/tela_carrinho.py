from entidade import cpf as cpf_util
from limite.tela_abstrata import TelaAbstrata

OPCOES = {
    1: "Criar um novo carrinho",
    2: "Comprar um produto",
    3: "Devolver um produto",
    4: "Listar carrinhos",
    5: "Finalizar carrinho",
    0: "Retornar",
}


class TelaCarrinho(TelaAbstrata):
    """Tela dos carrinhos.

    A versão anterior usava `input()` e `print()` aqui dentro, no meio de um
    aplicativo gráfico: pegar a quantidade ou o id do produto pedia digitação no
    terminal, atrás da janela. Agora tudo passa pela mesma interface.
    """

    def tela_opcoes(self) -> int:
        return self._menu("Mercado P&P", "Carrinhos", OPCOES)

    def pega_cpf(self, titulo: str = "Selecionar carrinho"):
        valores = self._formulario(titulo, titulo, [("cpf", "CPF do cliente:")])
        if valores is None:
            return None
        try:
            return cpf_util.normaliza(valores["cpf"])
        except cpf_util.CpfInvalidoError:
            self.mostra_erro("CPF inválido. Digite os 11 dígitos, com ou sem pontuação.")
            return None

    def pega_id_produto(self, titulo: str = "Selecionar produto do carrinho"):
        valores = self._formulario(titulo, titulo, [("id", "ID do produto:")])
        if valores is None:
            return None
        return self._para_inteiro(valores["id"], "O ID")

    def lista_carrinhos(self, carrinhos: list):
        if not carrinhos:
            self.mostra_mensagem("Nenhum carrinho registrado ainda.")
            return
        blocos = []
        for dados in carrinhos:
            blocos.append(self._formata_carrinho(dados))
        self.mostra_tabela("Lista de carrinhos", "\n\n".join(blocos))

    def mostra_carrinho(self, dados: dict):
        self.mostra_tabela(f"Carrinho de {dados['cliente_nome']}", self._formata_carrinho(dados))

    @staticmethod
    def _formata_carrinho(dados: dict) -> str:
        linhas = [
            f"Cliente: {dados['cliente_nome']}",
            f"CPF:     {cpf_util.formata(dados['cliente_cpf'])}",
        ]
        if not dados["itens"]:
            linhas.append("  Este carrinho está vazio, adicione alguns produtos!")
            return "\n".join(linhas)
        linhas.append(f"{'ID':<5}{'Nome':<28}{'Preço':>10}{'Qtd':>10}{'Subtotal':>12}")
        linhas.append("-" * 65)
        for item in dados["itens"]:
            linhas.append(
                f"{item['produto_id']:<5}{item['nome']:<28}{item['preco_unitario']:>10,.2f}"
                f"{item['quantidade']:>10,.3f}{item['subtotal']:>12,.2f}"
            )
        linhas.append("-" * 65)
        linhas.append(f"{'Total':<43}{dados['total']:>22,.2f}")
        return "\n".join(linhas)
