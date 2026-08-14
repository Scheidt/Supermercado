from limite.tela_abstrata import TelaAbstrata

OPCOES = {
    1: "Produtos",
    2: "Clientes",
    3: "Carrinhos",
    0: "Encerrar o sistema",
}


class TelaSistema(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._menu("Mercado P&P", "Bem-vindo ao Mercado P&P!", OPCOES)
