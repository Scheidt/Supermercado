"""Unidade de venda de um produto.

Existia como texto livre, comparado com literais diferentes em arquivos
diferentes ("Unidade(s)" no controlador, "Unitário(s)" na entidade), e por isso
o arredondamento de produto unitário nunca acontecia. Como Enum, a comparação
não tem como divergir.
"""
from enum import Enum


class Unidade(Enum):
    UNIDADE = "Unidade(s)"
    QUILOGRAMA = "Kg"
    LITRO = "L"

    @property
    def fracionavel(self) -> bool:
        # Um produto unitário só pode ser vendido em quantidades inteiras.
        return self is not Unidade.UNIDADE

    @classmethod
    def de_texto(cls, texto) -> "Unidade":
        if isinstance(texto, cls):
            return texto
        chave = str(texto).strip().casefold()
        try:
            return _SINONIMOS[chave]
        except KeyError:
            validas = ", ".join(u.value for u in cls)
            raise ValueError(f"Unidade desconhecida: {texto!r}. Use uma de: {validas}.")

    def __str__(self) -> str:
        return self.value


_SINONIMOS = {
    "unidade": Unidade.UNIDADE,
    "unidades": Unidade.UNIDADE,
    "unidade(s)": Unidade.UNIDADE,
    "unitario": Unidade.UNIDADE,
    "unitário": Unidade.UNIDADE,
    "un": Unidade.UNIDADE,
    "unid": Unidade.UNIDADE,
    "kg": Unidade.QUILOGRAMA,
    "quilo": Unidade.QUILOGRAMA,
    "quilos": Unidade.QUILOGRAMA,
    "quilograma": Unidade.QUILOGRAMA,
    "quilogramas": Unidade.QUILOGRAMA,
    "l": Unidade.LITRO,
    "litro": Unidade.LITRO,
    "litros": Unidade.LITRO,
}
