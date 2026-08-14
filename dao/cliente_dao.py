from dao.abstract_dao import AbstractDAO
from entidade.cliente import Cliente


class ClienteDAO(AbstractDAO):
    def __init__(self, diretorio=None):
        super().__init__("clientes.json", diretorio)

    def _chave(self, cliente: Cliente) -> str:
        if not isinstance(cliente, Cliente):
            raise TypeError(f"Esperado Cliente, recebido {type(cliente).__name__}.")
        return cliente.cpf

    def _serializa(self, cliente: Cliente) -> dict:
        return cliente.to_dict()

    def _desserializa(self, dados: dict) -> Cliente:
        return Cliente.from_dict(dados)
