from abc import ABC, abstractmethod

class EstrategiaCobro(ABC):
    @abstractmethod
    def calcular_precio(self, precio_base: float) -> float:
        pass
