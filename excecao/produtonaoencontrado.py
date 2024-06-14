

class ProdutoNaoEncontradoException(Exception):
    def __init__(self) -> None:
        super().__init__("Não foi encontrado produto para esta ID.")