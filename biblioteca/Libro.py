from dataclasses import dataclass
from biblioteca.Autor import Autor

@dataclass
class Libro:
    _titulo: str
    _autor: Autor
    _isbn: str
    _categoria: str = "novela"
    _disponible: bool = True

    @property
    def titulo(self): return self._titulo

    @property
    def autor(self): return self._autor

    @property
    def isbn(self): return self._isbn

    @property
    def categoria(self): return self._categoria

    @property
    def disponible(self): return self._disponible

    def prestar(self): self._disponible = False

    def devolver(self): self._disponible = True

    def __str__(self):
        return f"'{self._titulo}' [{self._categoria}]"
