from dataclasses import dataclass, field
from biblioteca.Persona import Persona
from biblioteca.Observer import Observer

@dataclass
class Socio(Persona, Observer):
    _numero_socio: int = 0
    _notificaciones: list[str] = field(default_factory=list)

    @property
    def numero_socio(self):
        return self._numero_socio
    
    @property
    def notificaciones(self):
        return self._notificaciones

    def descripcion(self) -> str:
        return f"Socio #{self._numero_socio}: {self._nombre}"
    
    def actualizar(self, mensaje: str):
        self._notificaciones.append(mensaje)
        print(f"📬 [{self._nombre}] {mensaje}")
    