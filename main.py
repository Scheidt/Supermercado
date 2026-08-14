"""Ponto de entrada do Mercado P&P."""
from controlador.controlador_sistema import ControladorSistema


def main():
    ControladorSistema().inicializa_sistema()


if __name__ == "__main__":
    main()
