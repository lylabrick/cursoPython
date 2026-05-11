from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.dto.PersonaDto import PersonaDTO
from services.impl.serviciosPersonaImpl import ServiciosPersonaImpl
from repository.SqlPersonaRepository import SQLPersonaRepository

router = APIRouter()

def get_persona_service(db: Session = Depends(get_db)):
    # Creamos el repositorio con la sesión de la base de datos
    repo = SQLPersonaRepository(db)
    # Retornamos la implementación del servicio pasándole el repositorio
    return ServiciosPersonaImpl(repo)

@router.get("/personas/{persona_id}", response_model=PersonaDTO)
def read_persona(persona_id: int, 
                service: ServiciosPersonaImpl = Depends(get_persona_service)):
    try:
        # Nota: Asegúrate de que buscarPersonaPorId esté definido en tu implementación
        return service.buscarPersonaPorId(persona_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))