"""Base das telas.

Duas mudanças estruturais em relação à versão anterior:

1. A janela deixou de ser atributo. Cada subclasse guardava `self.__window`, que
   o name mangling mandava para `_TelaProduto__window` em vez do
   `_TelaAbstrata__window` da property da base, deixando a property inalcançável.
   Uma janela vive só durante uma interação, então virou variável local de
   `_abre`, fechada num `finally`.

2. As conversões passaram a devolver None em vez de avisar e converter assim
   mesmo. O código antigo mostrava "insira um valor numérico" e chamava
   `int(texto)` na linha seguinte, derrubando o programa.
"""
from abc import ABC, abstractmethod

import FreeSimpleGUI as sg

TEMA = "DarkTeal4"
FONTE_TITULO = ("Helvetica", 20)
FONTE_TEXTO = ("Helvetica", 12)
FONTE_TABELA = ("Consolas", 11)
LARGURA_ROTULO = (14, 1)
LARGURA_CAMPO = (30, 1)

_CANCELAR = "Cancelar"
_CONFIRMAR = "Confirmar"


class TelaAbstrata(ABC):
    def __init__(self):
        sg.theme(TEMA)

    @abstractmethod
    def tela_opcoes(self) -> int:
        """Devolve a opção escolhida no menu. 0 significa voltar."""

    # --- janelas ------------------------------------------------------------

    def _abre(self, titulo: str, layout: list):
        """Abre a janela, lê uma vez e fecha, mesmo se a leitura falhar."""
        janela = sg.Window(titulo, layout, finalize=True)
        try:
            return janela.read()
        finally:
            janela.close()

    def _menu(self, titulo: str, cabecalho: str, opcoes: dict) -> int:
        """Monta um menu de rádios a partir de {valor: rótulo}."""
        layout = [
            [sg.Text(cabecalho, font=FONTE_TITULO)],
            [sg.Text("Escolha uma opção:", font=FONTE_TEXTO)],
        ]
        for indice, (valor, rotulo) in enumerate(opcoes.items()):
            layout.append([sg.Radio(rotulo, "opcoes", key=str(valor), default=(indice == 0))])
        layout.append([sg.Button(_CONFIRMAR), sg.Cancel(_CANCELAR)])

        evento, valores = self._abre(titulo, layout)
        if self._cancelou(evento, valores):
            return 0
        for valor in opcoes:
            if valores.get(str(valor)):
                return valor
        return 0

    def _formulario(self, titulo: str, cabecalho: str, campos: list):
        """Formulário simples. `campos` é uma lista de (chave, rótulo).

        Devolve o dicionário de valores brutos, ou None se o usuário cancelar.
        """
        layout = [[sg.Text(cabecalho, font=FONTE_TITULO)]]
        for chave, rotulo in campos:
            layout.append(
                [sg.Text(rotulo, size=LARGURA_ROTULO), sg.InputText("", key=chave, size=LARGURA_CAMPO)]
            )
        layout.append([sg.Button(_CONFIRMAR), sg.Cancel(_CANCELAR)])

        evento, valores = self._abre(titulo, layout)
        if self._cancelou(evento, valores):
            return None
        return valores

    @staticmethod
    def _cancelou(evento, valores) -> bool:
        return evento in (None, sg.WIN_CLOSED, _CANCELAR) or valores is None

    # --- mensagens ----------------------------------------------------------

    def mostra_mensagem(self, mensagem: str, titulo: str = "Mercado P&P"):
        sg.popup_ok(mensagem, title=titulo)

    def mostra_erro(self, mensagem: str, titulo: str = "Erro"):
        sg.popup_error(mensagem, title=titulo)

    def mostra_tabela(self, titulo: str, texto: str):
        """Texto tabular em fonte monoespaçada, senão o alinhamento não fecha."""
        sg.popup_scrolled(texto, title=titulo, font=FONTE_TABELA, size=(80, 25))

    # --- conversões ---------------------------------------------------------

    def _para_inteiro(self, valor, rotulo: str):
        """Converte para int, ou avisa e devolve None."""
        try:
            return int(str(valor).strip())
        except (TypeError, ValueError):
            self.mostra_erro(f"{rotulo} deve ser um número inteiro.")
            return None

    def _para_decimal(self, valor, rotulo: str):
        """Converte para float aceitando vírgula decimal, ou avisa e devolve None."""
        try:
            return float(str(valor).strip().replace(",", "."))
        except (TypeError, ValueError):
            self.mostra_erro(f"{rotulo} deve ser um número.")
            return None

    def _texto_obrigatorio(self, valor, rotulo: str):
        """Devolve o texto sem espaços nas pontas, ou avisa e devolve None.

        Substitui o antigo `verificarString`, que chamava `str()` dentro de um
        try: como `str()` não levanta exceção para nenhuma entrada, a validação
        aprovava qualquer coisa, inclusive campo vazio.
        """
        texto = str(valor or "").strip()
        if not texto:
            self.mostra_erro(f"{rotulo} não pode ficar em branco.")
            return None
        return texto
