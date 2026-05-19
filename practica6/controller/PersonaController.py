from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.dto.PersonaDto import PersonaDTO, ClienteDTO, MiembroDTO
from services.impl.serviciosPersonaImpl import ServiciosPersonaImpl
from repository.impl.SqlPersonaRepository import SQLPersonaRepository


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

@router.post("/cliente", response_model=ClienteDTO)
def create_cliente(cliente: ClienteDTO, 
                    service: ServiciosPersonaImpl = Depends(get_persona_service)):
    try:
        return service.agregarCliente(cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/miembro", response_model=MiembroDTO)
def create_miembro(miembro: MiembroDTO, 
                    service: ServiciosPersonaImpl = Depends(get_persona_service)):
    try:
        return service.agregarMiembro(miembro)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))        

@router.get("/buscarPersonaPorDni/{dni}")
def buscarPersonaPorDni(dni: int, 
                        service: ServiciosPersonaImpl = Depends(get_persona_service)):
    try:
        return service.buscarPersonaPorDni(dni)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/buscarPersonaPorNombre/{nombre}")
def buscarPersonaPorNombre(nombre: str, 
                        service: ServiciosPersonaImpl = Depends(get_persona_service)):
    try:
        return service.buscarPersonaPorNombre(nombre)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/personas/{persona_id}/intereses/{interes}", response_model=PersonaDTO)
def update_intereses_persona(persona_id: int, 
                               interes: str, 
                               service: ServiciosPersonaImpl = Depends(get_persona_service)):
    """
    Agrega un nuevo interés a una persona existente.
    El interés se almacena como JSON en la base de datos.
    """
    try:
        return service.agregarInteres(persona_id, interes)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
