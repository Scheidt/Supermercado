from DAOs.abstractDAO import AbstractDAO
from entidade.produto import Produto

class ProdutoDAO(AbstractDAO):
    def __init__(self):
        super().__init__('produtos.pkl')

    def add(self, produto: dict):
        if (isinstance(produto['produto'].id, int)) and (produto is not None) and isinstance(produto['produto'], Produto):
            super().add(produto['produto'].id, produto)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)
    
    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)