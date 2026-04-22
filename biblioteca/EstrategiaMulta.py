
from abc import ABC, abstractmethod
from biblioteca.Libro import Libro

class EstrategiaMulta(ABC):
    @abstractmethod
    def calcular(self, dias_retraso: int, libro: "Libro") -> float:
        pass

    @abstractmethod
    def descripcion(self) -> str:
        pass
