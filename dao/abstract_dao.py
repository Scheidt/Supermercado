"""Repositório genérico com persistência em JSON.
"""
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

DIRETORIO_DADOS = Path(__file__).resolve().parent.parent / "dados"


class ChaveDuplicadaError(ValueError):
    def __init__(self, chave):
        super().__init__(f"Já existe um registro com a chave {chave!r}.")
        self.chave = chave


class RegistroNaoEncontradoError(LookupError):
    def __init__(self, chave):
        super().__init__(f"Não há registro com a chave {chave!r}.")
        self.chave = chave


class AbstractDAO(ABC):
    def __init__(self, arquivo: str, diretorio: Path = None):
        self._caminho = Path(diretorio or DIRETORIO_DADOS) / arquivo
        self._cache = {}
        self._carregar()

    # --- contrato das subclasses -------------------------------------------

    @abstractmethod
    def _chave(self, objeto):
        """A chave primária do objeto."""

    @abstractmethod
    def _serializa(self, objeto) -> dict:
        """Converte o objeto em um dicionário JSON."""

    @abstractmethod
    def _desserializa(self, dados: dict):
        """Reconstrói o objeto a partir do dicionário."""

    def _metadados(self) -> dict:
        """Campos extras gravados junto dos registros (sequências, por exemplo)."""
        return {}

    def _le_metadados(self, conteudo: dict):
        """Lê de volta o que `_metadados` gravou."""

    # --- operações ----------------------------------------------------------

    def add(self, objeto):
        chave = self._chave(objeto)
        if chave in self._cache:
            raise ChaveDuplicadaError(chave)
        self._cache[chave] = objeto
        self.salvar()

    def update(self, objeto):
        #Grava em disco as alterações feitas no objeto.
        
        chave = self._chave(objeto)
        if chave not in self._cache:
            raise RegistroNaoEncontradoError(chave)
        self._cache[chave] = objeto
        self.salvar()

    def get(self, chave):
        """Devolve o registro, ou None se não existir."""
        return self._cache.get(chave)

    def remove(self, chave):
        # Remove o registro e o devolve.
        # Levanta RegistroNaoEncontradoError se não houver nada com essa chave.
    
        if chave not in self._cache:
            raise RegistroNaoEncontradoError(chave)
        objeto = self._cache.pop(chave)
        self.salvar()
        return objeto

    def get_all(self) -> list:
        return list(self._cache.values())

    def salvar(self):
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        conteudo = dict(self._metadados())
        conteudo["registros"] = [self._serializa(o) for o in self._cache.values()]
        temporario = self._caminho.with_suffix(self._caminho.suffix + ".tmp")
        with open(temporario, "w", encoding="utf-8") as arquivo:
            json.dump(conteudo, arquivo, ensure_ascii=False, indent=2)
        os.replace(temporario, self._caminho)

    def _carregar(self):
        try:
            with open(self._caminho, encoding="utf-8") as arquivo:
                conteudo = json.load(arquivo)
        except FileNotFoundError:
            return
        except json.JSONDecodeError as erro:
            raise ValueError(f"Arquivo de dados corrompido: {self._caminho}") from erro
        if not isinstance(conteudo, dict) or "registros" not in conteudo:
            raise ValueError(f"Arquivo de dados corrompido: {self._caminho}")
        self._le_metadados(conteudo)
        for dados in conteudo["registros"]:
            objeto = self._desserializa(dados)
            self._cache[self._chave(objeto)] = objeto

    def __len__(self) -> int:
        return len(self._cache)

    def __contains__(self, chave) -> bool:
        return chave in self._cache

    def __iter__(self):
        return iter(self._cache.values())
