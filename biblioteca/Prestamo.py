from dataclasses import dataclass
from datetime import date
from biblioteca.Libro import Libro
from biblioteca.Socio import Socio

@dataclass
class Prestamo:
    _libro: Libro
    _socio: Socio
    _fecha_inicio: date
    _fecha_limite: date
    _fecha_devolucion: date = None

    @property
    def libro(self): return self._libro

    @property
    def socio(self): return self._socio

    @property
    def activo(self): return self._fecha_devolucion is None

    def devolver(self, fecha: date = None):
        self._fecha_devolucion = fecha or date.today()
        self._libro.devolver()

    def __str__(self):
        estado = "activo" if self.activo else f"devuelto el {self._fecha_devolucion}"
        return f"Préstamo de '{self._libro.titulo}' a {self._socio.nombre} [{estado}]"
