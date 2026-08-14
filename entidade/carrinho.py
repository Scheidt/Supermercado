from entidade import cpf as cpf_util
from entidade.item_carrinho import ItemCarrinho


class Carrinho:
    # Carrinho de um cliente, identificado pelo CPF dele.
    def __init__(self, cliente_cpf: str, itens=None):
        self.__cliente_cpf = cpf_util.normaliza(cliente_cpf)
        self.__itens: list[ItemCarrinho] = list(itens) if itens else []

    @property
    def cliente_cpf(self) -> str:
        return self.__cliente_cpf

    @property
    def itens(self) -> tuple:
        # Cópia somente leitura: alterar itens é responsabilidade do carrinho.
        return tuple(self.__itens)

    @property
    def vazio(self) -> bool:
        return not self.__itens

    @property
    def total(self) -> float:
        return round(sum(item.subtotal for item in self.__itens), 2)

    def item(self, produto_id: int):
        # Devolve o item daquele produto, ou None se não estiver no carrinho.
        for item in self.__itens:
            if item.produto_id == produto_id:
                return item
        return None

    def adicionar(self, item: ItemCarrinho):
        # Inclui o item, somando à linha existente se o produto já estiver aqui.
        if not isinstance(item, ItemCarrinho):
            raise TypeError(f"Esperado ItemCarrinho, recebido {type(item).__name__}.")
        existente = self.item(item.produto_id)
        if existente is None:
            self.__itens.append(item)
        else:
            existente.quantidade = existente.quantidade + item.quantidade

    def remover(self, produto_id: int) -> ItemCarrinho:
        # Tira o item do carrinho e devolve, para o estoque poder ser refeito.
        item = self.item(produto_id)
        if item is None:
            raise KeyError(f"Não há produto com id {produto_id} neste carrinho.")
        self.__itens.remove(item)
        return item

    def to_dict(self) -> dict:
        return {
            "cliente_cpf": self.__cliente_cpf,
            "itens": [item.to_dict() for item in self.__itens],
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Carrinho":
        return cls(
            cliente_cpf=dados["cliente_cpf"],
            itens=[ItemCarrinho.from_dict(i) for i in dados.get("itens", [])],
        )

    def __repr__(self) -> str:
        return f"Carrinho(cliente_cpf={self.__cliente_cpf!r}, itens={len(self.__itens)})"
