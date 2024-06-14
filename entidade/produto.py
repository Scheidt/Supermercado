class Produto():
    def __init__(self, nome: str, id: int, preco: float, unidade: str):
        self.__nome = nome
        self.__id = id
        self.__preco = preco
        self.__unidade = unidade
        
    @property
    def nome(self):
        return self.__nome

    @property
    def id(self):
        return self.__id

    @property
    def preco(self):
        return self.__preco

    @property
    def unidade(self):
        return self.__unidade

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @id.setter
    def id(self, id: int):
        self.__id = id

    @preco.setter
    def preco(self, preco: float):
        self.__preco = preco

    @unidade.setter
    def unidade(self, unidade: str):
        self.__unidade = unidade