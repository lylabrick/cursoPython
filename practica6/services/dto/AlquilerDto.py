from datetime import date
from services.dto.PeliculaDto import PeliculaDTO
from services.dto.PersonaDto import ClienteDTO
from pydantic import BaseModel, ConfigDict, Field

class AlquilerDTO(BaseModel):
    pelicula: PeliculaDTO
    cliente: ClienteDTO
    fecha_alquiler: date = Field(..., alias="fechaAlquiler") # Coincide con tu @property
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)