from services.entities.entidades import Pelicula, Persona, Alquiler

from typing import Protocol

class ServicioPelicula(Protocol):
    
    def agregarPeliculaANegocio(self, pelicula: Pelicula) -> Pelicula:
        ...

    def devolverPeliculaANegocio(self, pelicula: Pelicula) -> Pelicula:
        ...
        
    def buscarPelicula(self, titulo: str) -> Pelicula:
        ...
        
    def buscarPorGenero(self, genero: str) -> list(Pelicula):
        ...
        
    def prestamoDePelicula(self, pelicula: Pelicula, persona: Persona) -> Alquiler:
        ...

    def devolucionDePelicula(self, pelicula: Pelicula) -> None:
        ...