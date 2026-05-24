from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from repository.impl.SqlPeliculaRepository import SQLPeliculaRepository
from services.dto.PeliculaDto import PeliculaDTO
from services.impl.serviciosPeliculaImpl import ServiciosPeliculaImpl
from database import get_db
from pydantic import BaseModel
from repository.impl.SqlPersonaRepository import SQLPersonaRepository
from services.dto.AlquilerDto import AlquilerDTO
from services.dto.PersonaDto import ClienteDTO, MiembroDTO
from typing import Union

router = APIRouter()

def get_pelicula_service(db: Session = Depends(get_db)):
    # Creamos el repositorio con la sesión de la base de datos
    repo_peli = SQLPeliculaRepository(db)
    repo_perso = SQLPersonaRepository(db)
    # Retornamos la implementación del servicio pasándole el repositorio
    return ServiciosPeliculaImpl(repo_peli, repo_perso)


@router.get("/pelicula/{pelicula_id}", response_model=PeliculaDTO)
def read_pelicula(pelicula_id: int, 
                service: ServiciosPeliculaImpl = Depends(get_pelicula_service)):
    try:
        return service.buscarPeliculaPorId(pelicula_id)  # ← service, no self
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/buscarPeliculaPorTitulo/{titulo}", response_model=list[PeliculaDTO])
def read_pelicula(titulo: str, 
                service: ServiciosPeliculaImpl = Depends(get_pelicula_service)):
    try:
        # Nota: Asegúrate de que buscarPeliculaPorId esté definido en tu implementación
        return service.buscarPeliculaPorTitulo(titulo)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/pelicula", response_model=PeliculaDTO)
def create_pelicula(pelicula: PeliculaDTO, 
                    service: ServiciosPeliculaImpl = Depends(get_pelicula_service)):
    try:
        return service.agregarPeliculaANegocio(pelicula)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/devolverPelicula/{pelicula_id}", response_model=PeliculaDTO)
def devolver_pelicula(pelicula_id: int, 
                    service: ServiciosPeliculaImpl = Depends(get_pelicula_service)):
    try:
        return service.devolverPeliculaANegocio(pelicula_id)
    except ValueError as e:
        print("ERROR DE VALIDACION REAL:", e)
        raise HTTPException(status_code=400, detail=str(e))


class RegistroEsperaRequest(BaseModel):
    dni: int
    pelicula_id: int

@router.post(
    "/registrarParaEspera", 
    status_code=status.HTTP_200_OK, 
    response_model=Union[ClienteDTO, MiembroDTO], 
)
def registrar_para_espera(datos: RegistroEsperaRequest, 
                service: ServiciosPeliculaImpl = Depends(get_pelicula_service)):
    try:
        # El service ya lanza `ValueError` cuando la película o la persona no existen.
        persona_dto = service.registrarParaEspera(datos.dni, datos.pelicula_id)
        # Si se llegó aquí, la inserción fue exitosa.
        return persona_dto
    except ValueError as exc:
        # Distinguimos los distintos mensajes que arroja el service
        msg = str(exc)
        if "no encontrada" in msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=msg,
            )
        elif "no soportado" in msg:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=msg,
            )
        else:  # cualquier otro ValueError (p.ej. ya en espera)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=msg,
            )


@router.post("/alquilar", response_model=AlquilerDTO)
def alquilar(datos: RegistroEsperaRequest, 
            service: ServiciosPeliculaImpl = Depends(get_pelicula_service)):
    try:
        # Usas datos.dni y datos.pelicula_id
        return service.alquilarPelicula(datos.dni, datos.pelicula_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))        

@router.get("/buscarPorGenero/{genero}", response_model=list[PeliculaDTO])
def buscarPorGenero(genero: str, service: ServiciosPeliculaImpl = Depends(get_pelicula_service)):
    try:
        return service.buscarPorGenero(genero)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
