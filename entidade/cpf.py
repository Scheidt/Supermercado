# Normalização e validação de CPF.
import re

_NAO_DIGITOS = re.compile(r"\D")


class CpfInvalidoError(ValueError):
    def __init__(self, valor):
        super().__init__(f"CPF inválido: {valor!r}")
        self.valor = valor


def normaliza(valor) -> str:
    """Devolve o CPF como 11 dígitos sem pontuação.

    Levanta CpfInvalidoError se o valor não for um CPF válido.
    """
    digitos = _NAO_DIGITOS.sub("", str(valor if valor is not None else ""))
    if len(digitos) != 11 or not _verificadores_conferem(digitos):
        raise CpfInvalidoError(valor)
    return digitos


def e_valido(valor) -> bool:
    try:
        normaliza(valor)
    except CpfInvalidoError:
        return False
    return True


def formata(cpf: str) -> str:
    # Formata 11 dígitos como 000.000.000-00.
    cpf = normaliza(cpf)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def _verificadores_conferem(digitos: str) -> bool:
    if digitos == digitos[0] * 11:  # 00000000000, 11111111111 e afins
        return False
    for tamanho in (9, 10):
        soma = sum(int(d) * (tamanho + 1 - i) for i, d in enumerate(digitos[:tamanho]))
        if (soma * 10) % 11 % 10 != int(digitos[tamanho]):
            return False
    return True
