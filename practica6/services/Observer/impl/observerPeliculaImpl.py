from services.Observer.observerPelicula import ObserverPelicula
from services.entities.entidades import Persona

class PersonaObserver(ObserverPelicula):
    def __init__(self, persona: Persona):
        self.persona = persona
        
    def actualizar(self, pelicula_id: int) -> None:
        print(f"[NOTIFICACIÓN] {self.persona.nombre} ({self.persona.email}): "
              f"La película con id {pelicula_id} ya está disponible para alquiler.")

              
    