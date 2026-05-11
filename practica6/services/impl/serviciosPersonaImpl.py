from services.serviciosPersona import ServicioPersona
from services.entities.entidades import Persona, Pelicula, Alquiler
from repository.PersonaRepository import PersonaRepository

class ServiciosPersonaImpl(ServicioPersona):

    def __init__(self, repository: PersonaRepository):
        self.repository = repository
        
    def agregarPersona(self, persona: Persona) -> Persona:
        return self.repository.save(persona)

    def buscarPersonaPorId(self, persona_id: int) -> Persona:
        persona = self.repository.find_by_id(persona_id)
        if not persona:
            raise ValueError(f"Persona con id {persona_id} no encontrada")
        return persona

    def buscarPersonaPorDni(self, dni: int) -> Persona:
        # Implementación pendiente en el repositorio si se requiere
        pass

    def buscarPersonaPorNombre(self, nombre: str) -> Persona:
        pass