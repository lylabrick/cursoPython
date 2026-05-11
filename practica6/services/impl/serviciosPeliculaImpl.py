from services.serviciosPelicula import ServicioPelicula
from services.entities.entidades import Pelicula, Persona, Alquiler

class ServiciosPeliculaImpl(ServicioPelicula):
    
    def agregarPeliculaANegocio(self, pelicula: Pelicula) -> Pelicula:
        pass

    def devolverPeliculaANegocio(self, pelicula: Pelicula) -> Pelicula:
        pass
        
    def buscarPelicula(self, titulo: str) -> Pelicula:
        pass
        
    def buscarPorGenero(self, genero: str) -> list(Pelicula):
        pass
        
    def prestamoDePelicula(self, pelicula: Pelicula, persona: Persona) -> Alquiler:
        pass

    def devolucionDePelicula(self, pelicula: Pelicula) -> None:
        pass