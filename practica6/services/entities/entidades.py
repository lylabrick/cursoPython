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

pelicula_clientes_interesados = Table(
    "pelicula_clientes_interesados",
    Base.metadata,
    Column("pelicula_id", ForeignKey("pelicula.id"), primary_key=True),
    Column("cliente_id", ForeignKey("cliente.id"), primary_key=True),
)
pelicula_miembros_interesados = Table(
    "pelicula_miembros_interesados",
    Base.metadata,
    Column("pelicula_id", ForeignKey("pelicula.id"), primary_key=True),
    Column("miembro_id", ForeignKey("miembro.id"), primary_key=True),
)

persona_id_seq = Sequence('persona_id_seq', start=1)

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
    clientes_interesados: Mapped[List["Cliente"]] = relationship(secondary="pelicula_clientes_interesados")
    miembros_interesados: Mapped[List["Miembro"]] = relationship(secondary="pelicula_miembros_interesados")

    @property
    def interesados(self) -> list:
        return self.clientes_interesados + self.miembros_interesados

    @property
    def observadores(self) -> list:
        from services.Observer.impl.observerPeliculaImpl import PersonaObserver
        return [PersonaObserver(persona) for persona in self.interesados]

    def agregar_observador(self, observer: ObserverPelicula) -> None:
        from services.Observer.impl.observerPeliculaImpl import PersonaObserver
        if isinstance(observer, PersonaObserver):
            persona = observer.persona
            if isinstance(persona, Cliente):
                if persona not in self.clientes_interesados:
                    self.clientes_interesados.append(persona)
            elif isinstance(persona, Miembro):
                if persona not in self.miembros_interesados:
                    self.miembros_interesados.append(persona)

    def quitar_observador(self, observer: ObserverPelicula) -> None:
        from services.Observer.impl.observerPeliculaImpl import PersonaObserver
        if isinstance(observer, PersonaObserver):
            persona = observer.persona
            if isinstance(persona, Cliente):
                if persona in self.clientes_interesados:
                    self.clientes_interesados.remove(persona)
            elif isinstance(persona, Miembro):
                if persona in self.miembros_interesados:
                    self.miembros_interesados.remove(persona)

    def notificar_observadores(self, pelicula_titulo: str) -> None:
        for observer in self.observadores:
            observer.actualizar(pelicula_titulo)

class Persona(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, persona_id_seq, primary_key=True, server_default=persona_id_seq.next_value())
    dni: Mapped[int] = mapped_column(unique=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str] = mapped_column(String(20))
    direccion: Mapped[str] = mapped_column(String(200))
    fecha_nacimiento: Mapped[date] = mapped_column(Date)
    # Guardamos la lista de intereses como JSON en la base de datos
    intereses: Mapped[list] = mapped_column(JSON, default=list)

    @property
    def estrategia(self):
        # Importación local para evitar importaciones circulares en Python
        from services.strategy.impl.cobroCliente import CobroCliente
        return CobroCliente()

    def calcular_cobro(self, precio_base: float) -> float:
        # Persona actúa como el CONTEXTO y delega en su estrategia actual
        return self.estrategia.calcular_precio(precio_base)       

class Cliente(Persona):
    __tablename__ = "cliente"
    nivelesporsubir: Mapped[int] = mapped_column(Integer, default=0)

    alquileres: Mapped[List["Alquiler"]] = relationship(back_populates="cliente")
    recomendaciones: Mapped[List["Recomendacion"]] = relationship(back_populates="cliente")

class Miembro(Persona):
    __tablename__ = "miembro"
    descuento: Mapped[float] = mapped_column(Float)

    # Sobrescribimos la propiedad de la clase base
    @property
    def estrategia(self):
        # Importación local para evitar importaciones circulares
        from services.strategy.impl.cobroMiembroImpl import CobroMiembro
        return CobroMiembro(self)

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