from dataclasses import dataclass, field
from biblioteca.Observable import Observable 
from biblioteca.Observer import Observer

@dataclass
class Libro(Observable):
    _titulo: str
    _autor: str
    _isbn: str
    _categoria: str = "novela"
    _disponible: bool = True
    _lista_espera: list[Observer] = field(default_factory=list)

    @property
    def titulo(self):
        return self._titulo
    
    @property
    def autor(self):
        return self._autor

    @property
    def isbn(self):
        return self._isbn    
    
    @property
    def categoria(self):
        return self._isbn

    @property
    def lista_espera(self):
        return self.lista_espera

    @property
    def disponible(self):
        return self._disponible
    
    def suscribir(self, observer: Observer):
        if observer not in self._lista_espera:
            self._lista_espera.append(observer)

    def desuscribir(self, observer: Observer):
        if observer in self._lista_espera:
            self._lista_espera.remove(observer)
    
    def notificar(self, mensaje: str):
        for observer in self._lista_espera:
            observer.actualizar(mensaje)

    def prestar(self):
        self._disponible = False

    def devolver(self):
        self._disponible = True
        self.notificar(f"El libro '{self._titulo}' ya esta disponible")

    def __str__(self):
        estado = "disponible" if self._disponible else "prestado"
        en_espera = len(self._lista_espera)
        return f"'{self._titulo}' [{estado}] - {en_espera} en lista de espera"
