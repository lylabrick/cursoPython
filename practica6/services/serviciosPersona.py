from services.entities.entidades import Persona, Cliente, Miembro
from typing import Protocol
from services.dto.PersonaDto import PersonaDTO

class ServicioPersona(Protocol):
    
    def agregarCliente(self, cliente: Cliente) -> Cliente:
        ...

    def agregarMiembro(self, miembro: Miembro) -> Miembro:
        ...

    def buscarPersonaPorId(self, persona_id: int) -> Persona:
        ...

    def buscarPersonaPorDni(self, dni: int) -> Persona:
        ...

    def buscarPersonaPorNombre(self, nombre: str) -> Persona:
        ...

    def agregarInteres(self, persona_id: int, interes: str) -> Persona:
        ...



