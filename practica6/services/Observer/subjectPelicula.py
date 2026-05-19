from abc import ABC, abstractmethod
from services.Observer.observerPelicula import ObserverPelicula

class SubjectPelicula(ABC):
    @abstractmethod
    def agregar_observador(self, observer: ObserverPelicula) -> None:
        pass
    @abstractmethod
    def quitar_observador(self, observer: ObserverPelicula) -> None:
        pass
    @abstractmethod
    def notificar_observadores(self, pelicula_titulo: str) -> None:
        pass 