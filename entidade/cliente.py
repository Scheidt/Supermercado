from entidade import cpf as cpf_util


class Cliente:
    def __init__(self, cpf: str, nome: str, total_compras: float = 0.0):
        self.__cpf = cpf_util.normaliza(cpf)
        self.nome = nome
        self.total_compras = total_compras

    @property
    def cpf(self) -> str:
        return self.__cpf

    @property
    def cpf_formatado(self) -> str:
        return cpf_util.formata(self.__cpf)

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        nome = str(nome).strip()
        if not nome:
            raise ValueError("O nome do cliente não pode ficar vazio.")
        self.__nome = nome

    @property
    def total_compras(self) -> float:
        return self.__total_compras

    @total_compras.setter
    def total_compras(self, valor):
        valor = float(valor)
        if valor < 0:
            raise ValueError("O total de compras não pode ser negativo.")
        self.__total_compras = round(valor, 2)

    def registrar_compra(self, valor) -> float:
        # Soma uma compra ao total gasto e devolve o novo total.
        valor = float(valor)
        if valor < 0:
            raise ValueError("O valor da compra não pode ser negativo.")
        self.__total_compras = round(self.__total_compras + valor, 2)
        return self.__total_compras

    def to_dict(self) -> dict:
        return {"cpf": self.__cpf, "nome": self.__nome, "total_compras": self.__total_compras}

    @classmethod
    def from_dict(cls, dados: dict) -> "Cliente":
        return cls(
            cpf=dados["cpf"],
            nome=dados["nome"],
            total_compras=dados.get("total_compras", 0.0),
        )

    def __repr__(self) -> str:
        return f"Cliente(cpf={self.__cpf!r}, nome={self.__nome!r})"
