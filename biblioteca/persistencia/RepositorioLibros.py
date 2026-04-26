from biblioteca.Libro import Libro
from abc import ABC, abstractmethod
from typing import Optional

class RepositorioLibros(ABC):
     @abstractmethod
     def guardar(self, libro: "Libro"):
        pass
     
     @abstractmethod
     def buscar_por_isbn(self, isbn: str) -> Optional["Libro"]:
         pass
     
     @abstractmethod
     def listar_todos(self) -> list["Libro"]:
         pass
     
     @abstractmethod
     def eliminar(self, isbn: str):
         pass
