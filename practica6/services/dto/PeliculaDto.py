from pydantic import BaseModel, ConfigDict, Field, field_validator

class PeliculaDTO(BaseModel):
    # Definimos los campos del DTO
    titulo: str = Field(..., min_length=1, max_length=200)
    anio: int = Field(..., gt=1888)  # Validación: mayor al año de la primera película
    director: str
    genero: str
    duracion_minutos: int = Field(..., alias="duracion") # Mapeo de nombre diferente
    estado: str

    # Configuración para compatibilidad con la entidad
    model_config = ConfigDict(
        from_attributes=True, # Permite leer desde las @property de la dataclass
        frozen=True           # Inmutable como un Record de Java
    )

    @field_validator('estado')
    @classmethod
    def validar_estado(cls, v: str) -> str:
        estados_validos = ['Disponible', 'Alquilada', 'Mantenimiento']
        if v not in estados_validos:
            raise ValueError(f'Estado debe ser uno de: {estados_validos}')
        return v

    @classmethod
    def from_entity(cls, pelicula: "Pelicula"):
        # Mapeo manual si los nombres no coinciden exactamente
        return cls(
            titulo=pelicula.titulo,
            anio=pelicula.anio,
            director=pelicula.director,
            genero=pelicula.genero,
            duracion_minutos=pelicula.duracion,
            estado=pelicula.estado,
        )