class Cliente():
    def __init__(self, nome: str, cpf: int, gasto = 0):
        self.__nome = nome
        self.__cpf = cpf
        self.__totalcompras = gasto
    
    @property
    def nome(self):
        return self.__nome

    @property
    def cpf(self):
        return self.__cpf

    @property
    def totalcompras(self):
        return self.__totalcompras

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome
    
    @cpf.setter
    def cpf(self, cpf: int):
        self.__cpf = cpf

    @totalcompras.setter
    def totalcompras(self, totalcompras):
        self.__totalcompras = totalcompras

    def comprou(self, valor_compra: float):
        try:
            self.__totalcompras += valor_compra
        except ValueError:
            self.__totalcompras += float(valor_compra)
