from DAOs.abstractDAO import AbstractDAO
from entidade.carrinho import Carrinho

class CarrinhoDAO(AbstractDAO):
    def __init__(self):
        super().__init__('carrinhos.pkl')

    def add(self, carrinho: Carrinho):
        if (isinstance(carrinho.cliente.cpf, int)) and (carrinho is not None) and isinstance(carrinho, Carrinho):
            super().add(carrinho.cliente.cpf, carrinho)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)
    
    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
