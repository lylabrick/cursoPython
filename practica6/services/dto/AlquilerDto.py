from datetime import date
from services.dto.PeliculaDto import PeliculaDTO
from services.dto.PersonaDto import PersonaDTO
from pydantic import BaseModel, ConfigDict, Field

class AlquilerDTO(BaseModel):
    pelicula: PeliculaDTO
    persona: PersonaDTO
    fecha_alquiler: date = Field(..., alias="fechaAlquiler") # Coincide con tu @property
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)