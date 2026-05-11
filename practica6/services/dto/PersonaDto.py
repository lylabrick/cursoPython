from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List

class PersonaDTO(BaseModel):
    # Definimos los campos que queremos exponer
    dni: int
    nombre: str
    email: EmailStr  # Validación automática de formato de correo
    intereses: List[str] = Field(default_factory=list)
    
    # Esta configuración es la clave para que funcione como en Java/Spring
    model_config = ConfigDict(
        from_attributes=True,  # Permite crear el DTO desde un objeto (la entidad)
        frozen=True            # Lo hace inmutable, como un Record de Java
    )

    @classmethod
    def from_entity(cls, persona: "Persona"):
        # Mapeo manual si los nombres no coinciden exactamente
        return cls(
            dni=persona.dni,
            nombre=persona.nombre,
            email=persona.email,
            intereses=persona.intereses
        )

class ClienteDTO(PersonaDTO):
    nivelesporsubir: int

    @classmethod
    def from_entity(cls, cliente: "Cliente"):
        return cls(
            dni=cliente.dni,
            nombre=cliente.nombre,
            email=cliente.email,
            intereses=cliente.intereses,
            nivelesporsubir=cliente.nivelesporsubir
        )

class MiembroDTO(PersonaDTO):
    descuento: float

    @classmethod
    def from_entity(cls, miembro: "Miembro"):
        return cls(
            dni=miembro.dni,
            nombre=miembro.nombre,
            email=miembro.email,
            intereses=miembro.intereses,
            descuento=miembro.descuento
        )