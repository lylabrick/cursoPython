from services.serviciosPersona import ServicioPersona
from repository.PersonaRepository import PersonaRepository
from services.dto.PersonaDto import ClienteDTO, MiembroDTO
from services.entities.entidades import Cliente, Miembro, Persona

class ServiciosPersonaImpl(ServicioPersona):

    def __init__(self, repository: PersonaRepository):
        self.repository = repository
    
    def agregarCliente(self, cliente: ClienteDTO) -> Cliente:
        return self.repository.save(cliente.to_entity())

    def agregarMiembro(self, miembro: MiembroDTO) -> Miembro:
        return self.repository.save(miembro.to_entity())

    def buscarPersonaPorId(self, persona_id: int) -> Persona:
        persona = self.repository.find_by_id(persona_id)
        if not persona:
            raise ValueError(f"Persona con id {persona_id} no encontrada")
        
        if isinstance(persona, Cliente):
            return ClienteDTO.from_entity(persona)
        elif isinstance(persona, Miembro):
            return MiembroDTO.from_entity(persona)

    def buscarPersonaPorDni(self, dni: int) -> Persona:
        persona = self.repository.find_by_dni(dni)
        if not persona:
            raise ValueError(f"Persona con dni {dni} no encontrada")
        
        if isinstance(persona, Cliente):
            return ClienteDTO.from_entity(persona)
        elif isinstance(persona, Miembro):
            return MiembroDTO.from_entity(persona)

    def buscarPersonaPorNombre(self, nombre: str) -> Persona:
        persona = self.repository.find_by_name(nombre)
        if not persona:
            raise ValueError(f"Persona con nombre {nombre} no encontrada")
        
        if isinstance(persona, Cliente):
            return ClienteDTO.from_entity(persona)
        elif isinstance(persona, Miembro):
            return MiembroDTO.from_entity(persona)
    
    def agregarInteres(self, persona_id: int, interes: str) -> Persona:
        persona = self.repository.find_by_id(persona_id)
        if not persona:
            raise ValueError(f"Persona con id {persona_id} no encontrada")
        
        persona.intereses = list(set(persona.intereses) | {interes})
        return self.repository.save(persona)