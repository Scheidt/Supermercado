from abc import ABC, abstractmethod
import PySimpleGUI as sg
import time


class TelaAbstrata (ABC):
    @abstractmethod
    def __init__(self):
        self.__window = None
        pass

    @abstractmethod
    def tela_opcoes():
        pass

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window):
        self.__window = window

    def verificarInt(self, talvezint: int):
        try:
            int(talvezint)
        except ValueError:
            return False
        else:
            return True
    
    def verificarFloat(self, talvezfloat: float):
        try:
            float(talvezfloat)
        except ValueError:
            return False
        else:
            return True

    def verificarString(self, talvezString: str):
        try:
            str(talvezString)
        except:
            return False
    
    def mostra_mensagem(self, mensagem: str, pop = True):
        if pop == True:
            sg.popup_annoying(mensagem)
        else:
            print (mensagem)

    def verifica_opção(self, ints_validos = []):
        while True:
            valor_lido = input("Insira a opção desejada: ")
            try:
                valor_int = int(valor_lido) #tenta transformar o valor lido em inteiro.
                if ints_validos and valor_int not in ints_validos:
                    raise ValueError 
                return valor_int
            except ValueError: #aqui cai se não for int ou se não for valido
                print("A opção selecionada não existe. Tente novamente")
                