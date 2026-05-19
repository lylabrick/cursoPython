# services/observer/ObserverPelicula.py

from abc import ABC, abstractmethod

class ObserverPelicula(ABC):
    @abstractmethod
    def actualizar(self, pelicula_titulo: str) -> None:
        pass
