from abc import ABC, abstractmethod
from typing import Optional
from biblioteca.Prestamo import Prestamo

class RepositorioPrestamos(ABC):
    @abstractmethod
    def guardar(self, prestamo: "Prestamo"):
        pass

    @abstractmethod
    def listar_archivos(self) -> list["Prestamo"]:
        pass

    @abstractmethod
    def buscar_archivo_por_isbn(self, isbn: str) -> Optional["Prestamo"]:
        pass