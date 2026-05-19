from abc import ABC, abstractmethod
from typing import List, Optional
from services.entities.entidades import Pelicula

class PeliculaRepository(ABC):
    @abstractmethod
    def save(self, pelicula: Pelicula) -> Pelicula:
        pass

    @abstractmethod
    def find_by_id(self, pelicula_id: int) -> Optional[Pelicula]:
        pass

    @abstractmethod
    def find_all(self) -> List[Pelicula]:
        pass

    @abstractmethod
    def delete(self, pelicula_id: int) -> bool:
        pass

    @abstractmethod
    def find_by_genero(self, genero: str) -> List[Pelicula]:
        pass