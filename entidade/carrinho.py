from entidade.cliente import Cliente
from entidade.produto import Produto


class Carrinho():
    def __init__(self, cliente: Cliente):
        if (isinstance(cliente, Cliente)):
            self.__cliente = cliente
        else:
            raise TypeError
        self.__produtos = []

    @property
    def cliente(self):
        return self.__cliente
    
    @property
    def produtos(self):
        return self.__produtos

    @cliente.setter
    def cliente(self, cliente: Cliente):
        if (isinstance(cliente, Cliente)):
            self.__cliente = cliente
        else:
            raise TypeError

    def incluir_produto(self, pacote: dict):
        produto = pacote['produto']
        quantidade = pacote['quantidade']
        if isinstance(produto, Produto):
            pass
        else:
            raise TypeError
        copia = self.pega_produto_por_id(produto.id)
        if copia is None:
            self.__produtos.append({'produto': produto,
                                    'quantidade': quantidade})
        else:
            if copia['produto'].unidade == "Unitário(s)":
                self.__produtos[self.__produtos.index(copia)]['quantidade'] += round(quantidade)
            else:
                self.__produtos[self.__produtos.index(copia)]['quantidade'] += quantidade

    def pega_produto_por_id(self, id: int):
        for i in range(len(self.__produtos)):
            if id == self.__produtos[i]['produto'].id:
                return self.__produtos[i]
        else:
            return None

    