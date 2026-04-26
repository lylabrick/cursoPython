from biblioteca.persistencia.RepositorioLibros import RepositorioLibros
from biblioteca.Libro import Libro
from typing import Optional


class RepositorioLibrosMemoria(RepositorioLibros):
    
    def __init__(self):
        self._libros: dict[str, "Libro"] = {}

    def guardar(self, libro: "Libro"):
        self._libros[libro.isbn] = libro

    def buscar_por_isbn(self, isbn: str) -> Optional["Libro"]:
        return self._libros.get(isbn)

    def listar_todos(self) -> list["Libro"]:
        return list(self._libros.values())

    def eliminar(self, isbn: str):
        self._libros.pop(isbn, None)