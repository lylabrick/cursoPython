from __future__ import annotations
from datetime import date
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Integer, Float, Date, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Pelicula(Base):
    __tablename__ = "pelicula"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    anio: Mapped[int] = mapped_column(Integer)
    director: Mapped[str] = mapped_column(String(100))
    genero: Mapped[str] = mapped_column(String(50))
    duracion: Mapped[int] = mapped_column(Integer)
    estado: Mapped[str] = mapped_column(String(20))

    # Relaciones
    alquileres: Mapped[List["Alquiler"]] = relationship(back_populates="pelicula")
    recomendaciones: Mapped[List["Recomendacion"]] = relationship(back_populates="pelicula")

class Persona(Base):
    __tablename__ = "persona"

    id: Mapped[int] = mapped_column(primary_key=True)
    dni: Mapped[int] = mapped_column(unique=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str] = mapped_column(String(20))
    direccion: Mapped[str] = mapped_column(String(200))
    fecha_nacimiento: Mapped[date] = mapped_column(Date)
    # Guardamos la lista de intereses como JSON en la base de datos
    intereses: Mapped[list] = mapped_column(JSON, default=list)

    # Configuración para Herencia (Polimorfismo)
    type: Mapped[str] = mapped_column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "persona",
        "polymorphic_on": "type",
    }

class Cliente(Persona):
    __tablename__ = "cliente"
    id: Mapped[int] = mapped_column(ForeignKey("persona.id"), primary_key=True)
    nivelesporsubir: Mapped[int] = mapped_column(Integer, default=0)

    alquileres: Mapped[List["Alquiler"]] = relationship(back_populates="cliente")
    recomendaciones: Mapped[List["Recomendacion"]] = relationship(back_populates="cliente")

    __mapper_args__ = {
        "polymorphic_identity": "cliente",
    }

class Miembro(Persona):
    __tablename__ = "miembro"
    id: Mapped[int] = mapped_column(ForeignKey("persona.id"), primary_key=True)
    descuento: Mapped[float] = mapped_column(Float)

    __mapper_args__ = {
        "polymorphic_identity": "miembro",
    }

class Recomendacion(Base):
    __tablename__ = "recomendacion"

    id: Mapped[int] = mapped_column(primary_key=True)
    pelicula_id: Mapped[int] = mapped_column(ForeignKey("pelicula.id"))
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    recomendacion: Mapped[str] = mapped_column(String(500))
    fecha: Mapped[date] = mapped_column(Date, default=date.today)

    pelicula: Mapped["Pelicula"] = relationship(back_populates="recomendaciones")
    cliente: Mapped["Cliente"] = relationship(back_populates="recomendaciones")

class Alquiler(Base):
    __tablename__ = "alquiler"

    id: Mapped[int] = mapped_column(primary_key=True)
    pelicula_id: Mapped[int] = mapped_column(ForeignKey("pelicula.id"))
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    
    fecha_alquiler: Mapped[date] = mapped_column(Date)
    calificacion: Mapped[Optional[int]] = mapped_column(Integer)
    comentario: Mapped[Optional[str]] = mapped_column(String(500))
    fecha_prestamo: Mapped[date] = mapped_column(Date)
    fecha_devolucion: Mapped[Optional[date]] = mapped_column(Date)

    pelicula: Mapped["Pelicula"] = relationship(back_populates="alquileres")
    cliente: Mapped["Cliente"] = relationship(back_populates="alquileres")