from dao.abstract_dao import AbstractDAO
from entidade.carrinho import Carrinho


class CarrinhoDAO(AbstractDAO):
    def __init__(self, diretorio=None):
        super().__init__("carrinhos.json", diretorio)

    def _chave(self, carrinho: Carrinho) -> str:
        if not isinstance(carrinho, Carrinho):
            raise TypeError(f"Esperado Carrinho, recebido {type(carrinho).__name__}.")
        return carrinho.cliente_cpf

    def _serializa(self, carrinho: Carrinho) -> dict:
        return carrinho.to_dict()

    def _desserializa(self, dados: dict) -> Carrinho:
        return Carrinho.from_dict(dados)
