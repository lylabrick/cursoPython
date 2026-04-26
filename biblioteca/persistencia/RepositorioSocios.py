from abc import ABC, abstractmethod
from typing import Optional
from biblioteca.Socio import Socio

class RepositorioSocios(ABC):
    @abstractmethod
    def guardar(self, socio: "Socio"):
        pass

    @abstractmethod
    def buscar_por_numero(self, numero_socio: int) -> Optional["Socio"]:
        pass

    @abstractmethod
    def listar_todos(self) -> list["Socio"]:
        pass