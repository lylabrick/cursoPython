
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def actualizar(self, mensaje: str):
        pass

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