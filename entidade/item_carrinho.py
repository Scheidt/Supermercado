from entidade.produto import Produto
from entidade.unidade import Unidade


class ItemCarrinho:
    def __init__(self, produto_id: int, nome: str, preco_unitario: float, unidade, quantidade: float):
        self.__produto_id = produto_id
        self.__nome = nome
        self.__preco_unitario = round(float(preco_unitario), 2)
        self.__unidade = Unidade.de_texto(unidade)
        self.quantidade = quantidade

    @classmethod
    def de_produto(cls, produto: Produto, quantidade: float) -> "ItemCarrinho":
        return cls(
            produto_id=produto.id,
            nome=produto.nome,
            preco_unitario=produto.preco,
            unidade=produto.unidade,
            quantidade=quantidade,
        )

    @property
    def produto_id(self) -> int:
        return self.__produto_id

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def preco_unitario(self) -> float:
        return self.__preco_unitario

    @property
    def unidade(self) -> Unidade:
        return self.__unidade

    @property
    def quantidade(self) -> float:
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        quantidade = float(quantidade)
        if not self.__unidade.fracionavel:
            quantidade = float(round(quantidade))
        if quantidade <= 0:
            raise ValueError("A quantidade de um item do carrinho deve ser maior que zero.")
        self.__quantidade = quantidade

    @property
    def subtotal(self) -> float:
        return round(self.__preco_unitario * self.__quantidade, 2)

    def to_dict(self) -> dict:
        return {
            "produto_id": self.__produto_id,
            "nome": self.__nome,
            "preco_unitario": self.__preco_unitario,
            "unidade": self.__unidade.value,
            "quantidade": self.__quantidade,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "ItemCarrinho":
        return cls(
            produto_id=dados["produto_id"],
            nome=dados["nome"],
            preco_unitario=dados["preco_unitario"],
            unidade=dados["unidade"],
            quantidade=dados["quantidade"],
        )

    def __repr__(self) -> str:
        return f"ItemCarrinho(produto_id={self.__produto_id}, quantidade={self.__quantidade})"
