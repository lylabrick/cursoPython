from dataclasses import dataclass

@dataclass
class Libro:
    _titulo: str
    _autor: str
    _isbn: str
    _disponible: bool = True

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
    def disponible(self):
        return self._disponible

    def prestar(self):
        self._disponible = False

    def devolver(self):
        self._disponible = True

    def __str__(self):
        estado = "disponible" if self._disponible else "prestado"
        return f"'{self._titulo}' de {self._autor.nombre} [{estado}]"
