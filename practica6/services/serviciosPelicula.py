from services.entities.entidades import Pelicula, Persona, Alquiler
from services.dto.PeliculaDto import PeliculaDTO

from typing import Protocol

class ServicioPelicula(Protocol):
    
    def agregarPeliculaANegocio(self, pelicula: PeliculaDTO) -> Pelicula:
        ...

    def buscarPeliculaPorId(self, pelicula_id: int) -> Pelicula:
        ...

    def devolverPeliculaANegocio(self, pelicula: Pelicula) -> Pelicula:
        ...
        
    def buscarPeliculaPorTitulo(self, titulo: str) -> Pelicula:
        ...
        
    def buscarPorGenero(self, genero: str) -> list[Pelicula]:
        ...
        
    def alquilarPelicula(self, pelicula: Pelicula, persona: Persona) -> Alquiler:
        ...

    def devolverDePelicula(self, pelicula: Pelicula) -> None:
        ...

    def registrarParaEspera(self, dni: int, pelicula_id: int) -> None:
        ...