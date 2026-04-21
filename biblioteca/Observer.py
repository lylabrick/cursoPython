
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def actualizar(self, mensaje: str):
        pass

