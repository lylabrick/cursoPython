from repository.PersonaRepository import PersonaRepository
from services.entities.entidades import Persona,Cliente,Miembro
from services.dto.PersonaDto import PersonaDTO
from typing import Optional

# Suponiendo que tienes un modelo de BD definido con SQLAlchemy llamado Persona
class SQLPersonaRepository(PersonaRepository):
    def __init__(self, db_session):
        self.session = db_session

    def save(self, persona: Persona) -> Persona:
        self.session.add(persona)
        self.session.commit()
        return persona

    def find_by_id(self, persona_id: int) -> Optional[Persona]:
        # 1. Buscamos primero en la tabla de clientes
        result = self.session.query(Cliente).filter_by(id=persona_id).first()
        if result:
            return result
        # 2. Si no es cliente, buscamos en la tabla de miembros
        return self.session.query(Miembro).filter_by(id=persona_id).first()

    def find_by_dni(self, dni: int) -> Optional[Persona]:
        # 1. Buscamos primero por DNI en la tabla de clientes
        result = self.session.query(Cliente).filter_by(dni=dni).first()
        if result:
            return result
        # 2. Si no es cliente, buscamos en la tabla de miembros
        return self.session.query(Miembro).filter_by(dni=dni).first()

    def find_all(self):
        # Retornamos la lista combinada de ambas tablas
        return self.session.query(Cliente).all() + self.session.query(Miembro).all()

    def delete(self, persona_id: int) -> bool:
        persona = self.find_by_id(persona_id)
        if persona:
            self.session.delete(persona)
            self.session.commit()
            return True
        return False
    
    def find_by_name(self, nombre: str) -> list[Persona]:
        # Formateamos el patrón de búsqueda para buscar coincidencias parciales
        patron = f"%{nombre}%"
        
        # Buscamos coincidencias en ambas tablas
        clientes = self.session.query(Cliente).filter(Cliente.nombre.ilike(patron)).all()
        miembros = self.session.query(Miembro).filter(Miembro.nombre.ilike(patron)).all()
        
        # Combinamos y retornamos la lista completa
        return clientes + miembros
