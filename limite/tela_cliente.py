import FreeSimpleGUI as sg

from entidade import cpf as cpf_util
from limite.tela_abstrata import TelaAbstrata, FONTE_TITULO, LARGURA_CAMPO, LARGURA_ROTULO

OPCOES = {
    1: "Cadastrar um cliente",
    2: "Alterar um cliente",
    3: "Excluir um cliente",
    4: "Listar clientes",
    5: "Listar clientes por gasto",
    0: "Retornar",
}


class TelaCliente(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._menu("Mercado P&P", "Clientes", OPCOES)

    def pega_cpf(self, titulo: str = "Selecionar cliente"):
        """Devolve o CPF com 11 dígitos, ou None se cancelar ou digitar errado."""
        valores = self._formulario(titulo, titulo, [("cpf", "CPF:")])
        if valores is None:
            return None
        return self._para_cpf(valores["cpf"])

    def entrar_dados_cliente(self):
        """Dados de um cliente novo, ou None se cancelar ou preencher errado."""
        valores = self._formulario(
            "Cadastro de cliente",
            "Dados do cliente",
            [("nome", "Nome:"), ("cpf", "CPF:")],
        )
        if valores is None:
            return None
        nome = self._texto_obrigatorio(valores["nome"], "O nome")
        if nome is None:
            return None
        cpf = self._para_cpf(valores["cpf"])
        if cpf is None:
            return None
        return {"nome": nome, "cpf": cpf}

    def altera_nome(self, cliente_nome: str):
        """Só o nome: o CPF identifica o cliente e não é editável."""
        layout = [
            [sg.Text("Alterar cliente", font=FONTE_TITULO)],
            [sg.Text("Nome:", size=LARGURA_ROTULO), sg.InputText(cliente_nome, key="nome", size=LARGURA_CAMPO)],
            [sg.Button("Confirmar"), sg.Cancel("Cancelar")],
        ]
        evento, valores = self._abre("Alterar cliente", layout)
        if self._cancelou(evento, valores):
            return None
        return self._texto_obrigatorio(valores["nome"], "O nome")

    def lista_clientes(self, clientes: list):
        if not clientes:
            self.mostra_mensagem("Nenhum cliente cadastrado ainda.")
            return
        linhas = [f"{'CPF':<16}{'Nome':<30}{'Total gasto':>14}", "-" * 60]
        for dados in clientes:
            linhas.append(f"{dados['cpf']:<16}{dados['nome']:<30}{dados['total_compras']:>14,.2f}")
        self.mostra_tabela("Lista de clientes", "\n".join(linhas))

    def lista_melhores(self, clientes: list):
        if not clientes:
            self.mostra_mensagem("Nenhum cliente cadastrado ainda.")
            return
        linhas = [f"{'#':<4}{'Nome':<30}{'Total gasto':>14}", "-" * 48]
        for posicao, dados in enumerate(clientes, start=1):
            linhas.append(f"{posicao:<4}{dados['nome']:<30}{dados['total_compras']:>14,.2f}")
        self.mostra_tabela("Clientes por gasto", "\n".join(linhas))

    def _para_cpf(self, valor):
        try:
            return cpf_util.normaliza(valor)
        except cpf_util.CpfInvalidoError:
            self.mostra_erro(
                "CPF inválido. Digite os 11 dígitos, com ou sem pontuação."
            )
            return None
