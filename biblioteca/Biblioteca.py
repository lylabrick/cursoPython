from __future__ import annotations
from dataclasses import dataclass
from biblioteca.Libro import Libro
from biblioteca.Socio import Socio
from biblioteca.Prestamo import Prestamo


class Biblioteca:
    def __init__(self, nombre:str):
        self._nombre = nombre
        self._libros: list[Libro] = []
        self._socios: list[Socio] = []
        self._prestamos: list[Prestamo] = []

    def agregar_libro(self, libro: Libro):
        self._libros.append(libro)

    def registrar_socio(self, socio: Socio):
        self._socios.append(socio)

    def prestar_libro(self, isbn:str, socio: Socio) -> Prestamo | None:
        libro = self._buscar_libro(isbn)
        if libro and libro.disponible:
            print(f"DEBUG: El objeto libro es: {libro}")
            print(f"DEBUG: El tipo de libro.prestar es: {type(libro.prestar)}")
            libro.prestar() # Aquí es donde falla
            prestamo = Prestamo(libro, socio)
            self._prestamos.append(prestamo)
            return prestamo
        return None
    
    def devolver_libro(self, isbn: str):
        for prestamo in self._prestamos:
            if prestamo.libro.isbn == isbn and prestamo.activo:
                prestamo.devolver()
                return
            
    def agregar_a_lista_de_espera(self, isbn: str, socio: Socio):
        libro = self._buscar_libro(isbn)
        if libro:
            libro.suscribir(socio)
            print(f"✅ {socio.nombre} agregado a lista de espera de '{libro.titulo}'")
    
    def libros_disponibles(self) -> list[Libro]:
        return[l for l in self._libros if l.disponible]
    
    def prestamos_activos(self) -> list[Prestamo]:
        return [p for p in self._prestamos if p.activo]
    
    def _buscar_libro(self, isbn: str) -> Libro | None:
        for libro in self._libros:
            if libro.isbn == isbn:
                return libro
        return None
    
    def __str__(self):
        return f"Biblioteca '{self._nombre}' - {len(self._libros)} libros, {len(self._socios)} socios"
    

    
