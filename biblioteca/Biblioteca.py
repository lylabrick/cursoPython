from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from biblioteca.Libro import Libro
from biblioteca.Socio import Socio
from biblioteca.Prestamo import Prestamo
from biblioteca.persistencia.RepositorioLibros import RepositorioLibros
from biblioteca.persistencia.RepositorioPrestamos import RepositorioPrestamos
from biblioteca.persistencia.RepositorioSocios import RepositorioSocios
from datetime import date, timedelta

@dataclass
class Biblioteca:
    DIAS_PRESTAMO = 7

    def __init__(self, 
                nombre:str, 
                repo_libros: RepositorioLibros, 
                repo_socios: RepositorioSocios,
                repo_prestamos: RepositorioPrestamos,            
    ):
        self._nombre = nombre
        self._repo_libros = repo_libros
        self._repo_socios = repo_socios
        self._repo_prestamos = repo_prestamos

    def agregar_libro(self, libro: Libro):
        self._repo_libros.guardar(libro)

    def registrar_socio(self, socio: Socio):
        self._repo_socios.guardar(socio)

    def prestar_libro(self, isbn:str, numero_socio: int) -> Optional[Prestamo]:
        libro = self._repo_libros.buscar_por_isbn(isbn)
        socio = self._repo_socios.buscar_por_numero(numero_socio)
        if libro and socio and libro.disponible:
            libro.prestar()
            self._repo_libros.guardar(libro)
            fecha_inicio = date.today()
            fecha_limite = fecha_inicio + timedelta(days=self.DIAS_PRESTAMO)
            prestamo = Prestamo(
                libro, socio,
                fecha_inicio,
                fecha_limite,
            )
            self._repo_prestamos.guardar(prestamo)
            return prestamo
        return None
    
    def devolver_libro(self, isbn: str, fecha: date = None) -> float:
        prestamo = self._repo_prestamos.buscar_activo_por_isbn(isbn)
        if prestamo:
            prestamo.devolver()
            self._repo_libros.guardar(prestamo.libro)
            self._repo_prestamos.guardar(prestamo)
    
    def libros_disponibles(self) -> list[Libro]:
        return [l for l in self._repo_libros.listar_todos() if l.disponible]
    
    def prestamos_activos(self):
        return self._repo_prestamos.listar_activos()
    
    def __str__(self):
        return f"Biblioteca '{self._nombre}'"
    

    
