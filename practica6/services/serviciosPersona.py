from services.entities.entidades import Persona
from typing import Protocol
from services.dto.PersonaDto import PersonaDTO

class ServicioPersona(Protocol):
    
    def agregarPersona(self, persona: Persona) -> Persona:
        ...

    def buscarPersonaPorId(self, persona_id: int) -> Persona:
        ...

    def buscarPersonaPorDni(self, dni: int) -> Persona:
        ...

    def buscarPersonaPorNombre(self, nombre: str) -> Persona:
        ...



