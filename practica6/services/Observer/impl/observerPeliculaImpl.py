from services.Observer.observerPelicula import ObserverPelicula
from services.entities.entidades import Persona

class PersonaObserver(ObserverPelicula):
    def __init__(self, persona: Persona):
        self.persona = persona
    def actualizar(self, pelicula_titulo: str) -> None:
        print(f"[NOTIFICACIÓN] {self.persona.nombre} ({self.persona.email}): "
              f"La película '{pelicula_titulo}' ya está disponible para alquiler.")

              
    