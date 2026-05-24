from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List, Literal, Union
from datetime import date

class PersonaDTO(BaseModel):
    # Definimos los campos que queremos exponer
    dni: int
    nombre: str
    email: EmailStr
    telefono: str              # ← Agregar
    direccion: str             # ← Agregar
    fecha_nacimiento: date     # ← Agregar
    intereses: List[str] = Field(default_factory=list)
    
    # Esta configuración es la clave para que funcione como en Java/Spring
    model_config = ConfigDict(
        from_attributes=True,  # Permite crear el DTO desde un objeto (la entidad)
        frozen=True            # Lo hace inmutable, como un Record de Java
    )

    @classmethod
    def from_entity(cls, persona: "Persona"):
        # Mapeo manual si los nombres no coinciden exactamente
        return PersonaDTO(
            dni=persona.dni,
            nombre=persona.nombre,
            email=persona.email,
            intereses=persona.intereses,
            telefono=persona.telefono,
            direccion=persona.direccion,
            fecha_nacimiento=persona.fecha_nacimiento,
        )

class ClienteDTO(PersonaDTO):
    type: Literal["cliente"] = "cliente"  # valor fijo
    nivelesporsubir: int

    @classmethod
    def from_entity(cls, persona: "Cliente"):
        # 1. Llamamos al from_entity del padre (PersonaDTO)
        persona_dto = super().from_entity(persona)
        # 2. Desglosamos sus campos y agregamos los del cliente
        return cls(
            **persona_dto.model_dump(), 
            nivelesporsubir=persona.nivelesporsubir
        )

    def to_entity(self) -> "Cliente":
        from services.entities.entidades import Cliente # Import local para evitar importación circular
        return Cliente(
            dni=self.dni,
            nombre=self.nombre,
            email=self.email,
            intereses=self.intereses,
            nivelesporsubir=self.nivelesporsubir,
            telefono=self.telefono,
            direccion=self.direccion,
            fecha_nacimiento=self.fecha_nacimiento,
        )

class MiembroDTO(PersonaDTO):
    type: Literal["miembro"] = "miembro"
    descuento: float
    @classmethod
    def from_entity(cls, persona: "Miembro"):
        # 1. Llamamos al from_entity del padre (PersonaDTO)
        persona_dto = super().from_entity(persona)
        # 2. Desglosamos sus campos y agregamos los del miembro
        return cls(
            **persona_dto.model_dump(), 
            descuento=persona.descuento
        )

    def to_entity(self) -> "Miembro":
        from services.entities.entidades import Miembro # Import local para evitar importación circular
        return Miembro(
            dni=self.dni,
            nombre=self.nombre,
            email=self.email,
            intereses=self.intereses,
            descuento=self.descuento,
            telefono=self.telefono,
            direccion=self.direccion,
            fecha_nacimiento=self.fecha_nacimiento
        )

PersonaResponse = Union[ClienteDTO, MiembroDTO]