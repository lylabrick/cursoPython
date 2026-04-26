from dataclasses import dataclass

from biblioteca.Persona import Persona

@dataclass
class Autor(Persona):
    _nacionalidad: str = ""

    @property
    def nacionalidad(self): return self._nacionalidad

    def descripcion(self) -> str:
        return f"Autor: {self._nombre} ({self._nacionalidad})"