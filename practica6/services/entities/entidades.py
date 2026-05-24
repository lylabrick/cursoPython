from __future__ import annotations
from datetime import date
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Float, Date, JSON, Sequence
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey

from services.Observer.subjectPelicula import SubjectPelicula
from services.Observer.observerPelicula import ObserverPelicula

class Base(DeclarativeBase):
    pass

pelicula_personas_interesadas = Table(
    "pelicula_personas_interesadas",
    Base.metadata,
    Column("pelicula_id", ForeignKey("pelicula.id"), primary_key=True),
    Column("persona_id", ForeignKey("persona.id"), primary_key=True),
)

class Pelicula(Base):
    __tablename__ = "pelicula"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    anio: Mapped[int] = mapped_column(Integer)
    director: Mapped[str] = mapped_column(String(100))
    genero: Mapped[str] = mapped_column(String(50))
    duracion: Mapped[int] = mapped_column(Integer)
    estado: Mapped[str] = mapped_column(String(20))
    precio: Mapped[float] = mapped_column(Float)

    # Relaciones
    alquileres: Mapped[List["Alquiler"]] = relationship(back_populates="pelicula")
    recomendaciones: Mapped[List["Recomendacion"]] = relationship(back_populates="pelicula")
    personas_interesadas: Mapped[List["Persona"]] = relationship(
        secondary="pelicula_personas_interesadas"
    )

    @property
    def interesados(self) -> list:
        return self.personas_interesadas

    @property
    def observadores(self) -> list:
        from services.Observer.impl.observerPeliculaImpl import PersonaObserver
        return [PersonaObserver(persona) for persona in self.personas_interesadas]

    def agregar_observador(self, observer: ObserverPelicula) -> None:
        from services.Observer.impl.observerPeliculaImpl import PersonaObserver
        if isinstance(observer, PersonaObserver):
            persona = observer.persona
            if persona not in self.personas_interesadas:
                self.personas_interesadas.append(persona)

    def quitar_observador(self, observer: ObserverPelicula) -> None:
        from services.Observer.impl.observerPeliculaImpl import PersonaObserver
        if isinstance(observer, PersonaObserver):
            persona = observer.persona
            if persona in self.personas_interesadas:
                self.personas_interesadas.remove(persona)

    def notificar_observadores(self, pelicula_id: int) -> None:
        for observer in self.observadores:
            print("SE NOTIFICO A LA PERSONA CON DNI ", observer.persona.dni)
            observer.actualizar(pelicula_id)
            self.quitar_observador(observer)

persona_id_seq = Sequence('persona_id_seq', start=1)

class Persona(Base):
    __tablename__ = "persona"
    __mapper_args__ = {
        "polymorphic_on": "tipo",
        "polymorphic_identity": "persona"
    }

    id: Mapped[int] = mapped_column(Integer, persona_id_seq, primary_key=True, server_default=persona_id_seq.next_value())
    tipo: Mapped[str] = mapped_column(String(20))  # columna discriminadora
    dni: Mapped[int] = mapped_column(unique=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str] = mapped_column(String(20))
    direccion: Mapped[str] = mapped_column(String(200))
    fecha_nacimiento: Mapped[date] = mapped_column(Date)
    intereses: Mapped[list] = mapped_column(JSON, default=list)

    # Campos de subclases — Optional porque no aplican a todos
    nivelesporsubir: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    descuento: Mapped[Optional[float]] = mapped_column(Float)

    # Relaciones
    alquileres: Mapped[List["Alquiler"]] = relationship(back_populates="persona")
    recomendaciones: Mapped[List["Recomendacion"]] = relationship(back_populates="persona")

    @property
    def estrategia(self):
        from services.strategy.impl.cobroClienteImpl import CobroCliente
        return CobroCliente()

    def calcular_cobro(self, precio_base: float) -> float:
        return self.estrategia.calcular_precio(precio_base)


class Cliente(Persona):
    __mapper_args__ = {
        "polymorphic_identity": "cliente"
    }

    @property
    def estrategia(self):
        from services.strategy.impl.cobroClienteImpl import CobroCliente
        return CobroCliente()


class Miembro(Persona):
    __mapper_args__ = {
        "polymorphic_identity": "miembro"
    }

    @property
    def estrategia(self):
        from services.strategy.impl.cobroMiembroImpl import CobroMiembro
        return CobroMiembro(self)

class Recomendacion(Base):
    __tablename__ = "recomendacion"

    id: Mapped[int] = mapped_column(primary_key=True)
    pelicula_id: Mapped[int] = mapped_column(ForeignKey("pelicula.id"))
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"))
    recomendacion: Mapped[str] = mapped_column(String(500))
    fecha: Mapped[date] = mapped_column(Date, default=date.today)

    pelicula: Mapped["Pelicula"] = relationship(back_populates="recomendaciones")
    persona: Mapped["Persona"] = relationship(back_populates="recomendaciones")

class Alquiler(Base):
 
    __tablename__ = "alquiler"

    id: Mapped[int] = mapped_column(primary_key=True)
    pelicula_id: Mapped[int] = mapped_column(ForeignKey("pelicula.id"))
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"))
    
    fecha_alquiler: Mapped[date] = mapped_column(Date)
    calificacion: Mapped[Optional[int]] = mapped_column(Integer)
    comentario: Mapped[Optional[str]] = mapped_column(String(500))
    fecha_prestamo: Mapped[date] = mapped_column(Date)
    fecha_devolucion: Mapped[Optional[date]] = mapped_column(Date)

    pelicula: Mapped["Pelicula"] = relationship(back_populates="alquileres")
    persona: Mapped["Persona"] = relationship(back_populates="alquileres")