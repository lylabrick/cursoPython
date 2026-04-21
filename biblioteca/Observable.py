from abc import ABC, abstractmethod
from biblioteca.Observer import Observer

class Observable(ABC):
    @abstractmethod
    def suscribir(self, observer: Observer):
        pass

    @abstractmethod
    def desuscribir(self, observer: Observer):
        pass

    @abstractmethod
    def notificar(self, mensaje: str):
        pass 