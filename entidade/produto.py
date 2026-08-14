from entidade.unidade import Unidade


class Produto:
    # Um produto do catálogo, com o próprio estoque.
    def __init__(self, id: int, nome: str, preco: float, unidade, estoque: float = 0.0):
        if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
            raise ValueError(f"Id de produto inválido: {id!r}")
        self.__id = id
        self.__unidade = Unidade.de_texto(unidade)
        self.nome = nome
        self.preco = preco
        self.__estoque = 0.0
        if estoque:
            self.repor(estoque)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def unidade(self) -> Unidade:
        return self.__unidade

    @unidade.setter
    def unidade(self, unidade):
        nova = Unidade.de_texto(unidade)
        if not nova.fracionavel:
            self.__estoque = float(round(self.__estoque))
        self.__unidade = nova

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        nome = str(nome).strip()
        if not nome:
            raise ValueError("O nome do produto não pode ficar vazio.")
        self.__nome = nome

    @property
    def preco(self) -> float:
        return self.__preco

    @preco.setter
    def preco(self, preco: float):
        preco = float(preco)
        if preco < 0:
            raise ValueError("O preço não pode ser negativo.")
        self.__preco = round(preco, 2)

    @property
    def estoque(self) -> float:
        return self.__estoque

    @property
    def esgotado(self) -> bool:
        return self.__estoque <= 0

    def normaliza_quantidade(self, quantidade) -> float:
        # Ajusta a quantidade à unidade do produto (inteira, se unitário).
        quantidade = float(quantidade)
        if not self.__unidade.fracionavel:
            quantidade = float(round(quantidade))
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return quantidade

    def repor(self, quantidade) -> float:
        # Devolve quantidade ao estoque e retorna o novo total.
        self.__estoque = round(self.__estoque + self.normaliza_quantidade(quantidade), 3)
        return self.__estoque

    def retirar(self, quantidade) -> float:
        # Retira do estoque o quanto for possível e devolve o que saiu de fato.
        # Retornar a quantidade efetivamente retirada é o que impede o caso em que
        # o cliente levava o produto sem o estoque ser descontado.
        
        quantidade = self.normaliza_quantidade(quantidade)
        retirada = min(quantidade, self.__estoque)
        self.__estoque = round(self.__estoque - retirada, 3)
        return retirada

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "nome": self.__nome,
            "preco": self.__preco,
            "unidade": self.__unidade.value,
            "estoque": self.__estoque,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Produto":
        return cls(
            id=dados["id"],
            nome=dados["nome"],
            preco=dados["preco"],
            unidade=dados["unidade"],
            estoque=dados.get("estoque", 0.0),
        )

    def __repr__(self) -> str:
        return f"Produto(id={self.__id}, nome={self.__nome!r}, estoque={self.__estoque})"
