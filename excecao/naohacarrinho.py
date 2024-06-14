

class NaoHaCarrinhoException(Exception):
    def __init__(self):
        super().__init__("Não há carrinho para este cpf.")