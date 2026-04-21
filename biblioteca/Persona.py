from dataclasses import dataclass
from datetime import date
from abc import ABC, abstractmethod

@dataclass
class Persona(ABC):
    _nombre: str
    _email: str

    @property
    def nombre(self):
        return self._nombre
    
    @property
    def email(self):
        return self._email
    
    @abstractmethod
    def descripcion(self) -> str:
        pass

    def __str__(self):
        return self.descripcion()