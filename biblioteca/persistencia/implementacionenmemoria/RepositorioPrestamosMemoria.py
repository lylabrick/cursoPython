from biblioteca.persistencia.RepositorioPrestamos import RepositorioPrestamos
from biblioteca.Prestamo import Prestamo
from typing import Optional

class RepositorioPrestamosMemoria(RepositorioPrestamos):
    def __init__(self):
        self._prestamos: list["Prestamo"] = []

    def guardar(self, prestamo: "Prestamo"):
        self._prestamos.append(prestamo)

    def listar_archivos(self) -> list["Prestamo"]:
        return [p for p in self._prestamos if p.activo]
    
    def buscar_archivo_por_isbn(self, isbn: str) -> Optional["Prestamo"]:
        for prestamo in self._prestamos: 
            if prestamo.libro.isbn == isbn and prestamo.activo:
                return prestamo
        return None