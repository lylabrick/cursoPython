from repository.PersonaRepository import PersonaRepository
from services.entities.entidades import Persona,Cliente,Miembro
from services.dto.PersonaDto import PersonaDTO
from typing import Optional

# Suponiendo que tienes un modelo de BD definido con SQLAlchemy llamado PersonaModel
class SQLPersonaRepository(PersonaRepository):
    def __init__(self, db_session):
        self.session = db_session

    def save(self, persona: 'Persona') -> 'Persona':
        self.session.add(persona)
        self.session.commit()
        return persona

    def find_by_id(self, persona_id: int) -> Optional['Persona']:
        result = self.session.query(Persona).filter_by(id=persona_id).first()
        if not result:
            return None
        return result

    def find_all(self):
        return self.session.query(Persona).all()

    def delete(self, persona_id: int) -> bool:
        persona = self.find_by_id(persona_id)
        if persona:
            self.session.delete(persona)
            self.session.commit()
            return True
        return False