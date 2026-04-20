from dataclasses import dataclass
from biblioteca.Persona import Persona

@dataclass
class Socio(Persona):
    _numero_socio: int = 0

    @property
    def numero_socio(self):
        return self._numero_socio
    
    def descripcion(self) -> str:
        return f"Socio #{self._numero_socio}: {self._nombre}"