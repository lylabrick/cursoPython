from dataclasses import dataclass, field
from datetime import date
from biblioteca.Libro import Libro
from biblioteca.Socio import Socio
from biblioteca.EstrategiaMulta import EstrategiaMulta

@dataclass
class Prestamo:
    _libro: Libro
    _socio: Socio
    _fecha_limite: date
    _estrategia_multa: EstrategiaMulta
    _fecha_inicio: date = field(default_factory=date.today)
    _fecha_devolucion: date = None

    @property
    def libro(self):
        return self._libro

    @property
    def socio(self):
        return self._socio

    @property
    def activo(self):
        return self._fecha_devolucion is None
    
    @property
    def dias_retraso(self) -> int:
        fecha_ref = self._fecha_devolucion or date.today()
        delta = (fecha_ref - self._fecha_limite).days
        return max(0, delta)

    def devolver(self, fecha: date = None):
        self._fecha_devolucion = date.today()
        self._libro.devolver()

    def __str__(self):
        estado = "activo" if self.activo else f"devuelto el {self._fecha_devolucion}"
        return (
            f"Préstamo de {self._libro.titulo} a {self._socio.nombre} [{estado}]"
            f"[{estado}] - retraso: {self.dias_retraso} dias"
        )
    
    def calcular_multa(self) -> float:
        return self._estrategia_multa.calcular(self.dias_retraso, self._libro)
    
    def cambiar_estrategia(self, estrategia: EstrategiaMulta):
        self._estrategia_multa = estrategia
