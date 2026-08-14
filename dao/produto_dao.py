from dao.abstract_dao import AbstractDAO
from entidade.produto import Produto


class ProdutoDAO(AbstractDAO):
    def __init__(self, diretorio=None):
        self.__sequencia = 0
        super().__init__("produtos.json", diretorio)
        # Se o arquivo veio sem a sequência, ela começa depois do maior id já usado.
        self.__sequencia = max(self.__sequencia, max(self._cache, default=0))

    def _chave(self, produto: Produto) -> int:
        if not isinstance(produto, Produto):
            raise TypeError(f"Esperado Produto, recebido {type(produto).__name__}.")
        return produto.id

    def _serializa(self, produto: Produto) -> dict:
        return produto.to_dict()

    def _desserializa(self, dados: dict) -> Produto:
        return Produto.from_dict(dados)

    def _metadados(self) -> dict:
        return {"sequencia_id": self.__sequencia}

    def _le_metadados(self, conteudo: dict):
        self.__sequencia = conteudo.get("sequencia_id", 0)

    def reserva_id(self) -> int:
        """Reserva o próximo id da sequência e o grava.

        A sequência é persistida de propósito: calcular o id a partir dos
        produtos existentes, como fazia a versão anterior, entrega a um produto
        novo o id de um produto excluído. O nome é `reserva` porque a chamada tem
        efeito: o id sai da sequência mesmo se o cadastro não for adiante.
        """
        self.__sequencia += 1
        self.salvar()
        return self.__sequencia

    def pega_por_nome(self, nome: str):
        alvo = str(nome).strip().casefold()
        for produto in self._cache.values():
            if produto.nome.casefold() == alvo:
                return produto
        return None
