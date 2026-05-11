from datetime import date
from services.dto.PeliculaDto import PeliculaDTO
from services.dto.PersonaDto import ClienteDTO
from pydantic import BaseModel, ConfigDict, Field

class CalificacionDTO(BaseModel):
    pelicula: PeliculaDTO 
    cliente: ClienteDTO
    calificacion: int = Field(..., ge=1, le=10) # Validación 1-10
    comentario: str
    fecha: date

    model_config = ConfigDict(from_attributes=True)