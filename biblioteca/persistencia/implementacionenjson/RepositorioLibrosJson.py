import json
from biblioteca.persistencia.RepositorioLibros import RepositorioLibros
import os
from biblioteca.Libro import Libro
from biblioteca.Autor import Autor
from typing import Optional

class RepositorioLibrosJson(RepositorioLibros):
    def __init__(self, ruta: str = "libros.json"):
        self._ruta = ruta
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        if not os.path.exists(self._ruta):
            self._escribir({})

    def _leer(self) -> dict:
        with open(self._ruta, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def _escribir(self, datos: dict):
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f , indent=2, ensure_ascii=False)
    
    def _serializar(self, libro: "Libro") -> dict:
        return {
            "titulo":     libro.titulo,
            "isbn":       libro.isbn,
            "categoria":  libro.categoria,
            "disponible": libro.disponible,
            "autor": {
                "nombre":       libro.autor.nombre,
                "email":        libro.autor.email,
                "nacionalidad": libro.autor.nacionalidad,
            }
        }
        
    def _deserializar(self, datos: dict) -> "Libro":
        autor = Autor(
            datos["autor"]["nombre"],
            datos["autor"]["email"],
            datos["autor"]["nacionalidad"]
        )
        return Libro(
            datos["titulo"],
            autor,
            datos["isbn"],
            datos["categoria"],
            datos["disponible"]
        )

    def guardar(self, libro: "Libro"):
        datos = self._leer()
        datos[libro.isbn] = self._serializar(libro)
        self._escribir(datos)

    def buscar_por_isbn(self, isbn: str) -> Optional["Libro"]:
        datos = self._leer()
        if isbn in datos:
            return self._deserializar(datos[isbn])
        return None

    def listar_todos(self) -> list["Libro"]:
        datos = self._leer()
        return [self._deserializar(d) for d in datos.values()]

    def eliminar(self, isbn: str):
        datos = self._leer()
        datos.pop(isbn, None)
        self._escribir(datos)