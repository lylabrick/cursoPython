from abc import ABC, abstractmethod
from typing import List, Optional
from services.entities.entidades import Persona

class PersonaRepository(ABC):
    @abstractmethod
    def save(self, persona: Persona) -> Persona:
        pass

    @abstractmethod
    def find_by_id(self, persona_id: int) -> Optional[Persona]:
        pass

    @abstractmethod
    def find_by_dni(self, dni: int) -> Optional[Persona]:
        pass

    @abstractmethod
    def find_all(self) -> List[Persona]:
        pass

    @abstractmethod
    def delete(self, persona_id: int) -> bool:
        pass