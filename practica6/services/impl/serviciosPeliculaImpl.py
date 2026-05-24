from typing import Union
from services.serviciosPelicula import ServicioPelicula
from services.entities.entidades import Pelicula, Persona, Alquiler
from repository.PersonaRepository import PersonaRepository
from repository.PeliculaRepository import PeliculaRepository
from services.dto.PeliculaDto import PeliculaDTO
from services.dto.AlquilerDto import AlquilerDTO
from services.dto.PersonaDto import ClienteDTO, MiembroDTO

class ServiciosPeliculaImpl(ServicioPelicula):
    
    def __init__(self, repository: PeliculaRepository, repo_persona: PersonaRepository):
        self.repository = repository
        self.repo_persona = repo_persona

    def agregarPeliculaANegocio(self, pelicula: PeliculaDTO) -> Pelicula:
        pelicula = pelicula.to_entity()
        return self.repository.save(pelicula)

    def devolverPeliculaANegocio(self, pelicula_id: int) -> Pelicula:
        pelicula = self.repository.find_by_id(pelicula_id)
        if not pelicula:
            raise ValueError(f"Pelicula con id {pelicula_id} no encontrada")

        pelicula.estado = "Disponible"
    
        pelicula.notificar_observadores(pelicula.id)

        # 5. Limpiamos la lista de interesados persistente en la BD
        pelicula.interesados.clear()
        
        # 6. Guardamos los cambios de la película en la base de datos
        self.repository.save(pelicula)
        return pelicula

    def buscarPeliculaPorTitulo(self, titulo: str) -> list[Pelicula]:
        peliculas = self.repository.find_by_titulo(titulo)
        if not peliculas:
            raise ValueError(f"Pelicula con titulo {titulo} no encontrada")
        
        return list(map(lambda p: PeliculaDTO.from_entity(p), peliculas))

    def buscarPorGenero(self, genero: str) -> list[Pelicula]:
        peliculas = self.repository.find_by_genero(genero)
        if not peliculas:
            raise ValueError(f"Pelicula con genero {genero} no encontrada")
        return list(map(lambda p: PeliculaDTO.from_entity(p), peliculas))

        
    def alquilarPelicula(self, dni: int, pelicula_id: int) -> AlquilerDTO:
        pelicula = self.repository.find_by_id(pelicula_id)
        if not pelicula:
            raise ValueError(f"Pelicula con id {pelicula_id} no encontrada")
        
        # 2. Validar disponibilidad
        if pelicula.estado != "Disponible":
            raise ValueError(f"La película '{pelicula.titulo}' no está disponible (estado: {pelicula.estado})")
        
        # 3. Buscar al persona por DNI
        persona = self.repo_persona.find_by_dni(dni)
        if not persona:
            raise ValueError(f"Persona con DNI {dni} no encontrado")
            
        # 4. Cambiar el estado de la película
        pelicula.estado = "Alquilada"

        # 5. Calcular cobro dinámicamente usando el patrón Strategy que creamos en tu Entidad
        precio_base = pelicula.precio  
        precio_final = persona.calcular_cobro(precio_base)
        print(f"\n--- TICKET DE COBRO ---")
        print(f"Cliente: {persona.nombre} (Tipo: {persona.__class__.__name__})")
        print(f"Película: {pelicula.titulo}")
        print(f"Total Cobrado: ${precio_final} (Estrategia: {persona.estrategia.__class__.__name__})")
        print(f"-----------------------\n")

        # 6. Crear el registro en la tabla Alquiler
        from datetime import date
        from services.entities.entidades import Alquiler
        from services.dto.AlquilerDto import AlquilerDTO
        
        nuevo_alquiler = Alquiler(
            pelicula=pelicula,
            persona=persona,
            fecha_alquiler=date.today(),
            fecha_prestamo=date.today()
        )
        
        # Guardar todo en la base de datos (SQLAlchemy guardará ambos en una transacción)
        self.repository.session.add(nuevo_alquiler)
        self.repository.save(pelicula)
        
        return AlquilerDTO.model_validate(nuevo_alquiler)
    
    def devolucionDePelicula(self, pelicula: Pelicula) -> None:
        pass

    def buscarPeliculaPorId(self, pelicula_id: int) -> Pelicula:
        pelicula = self.repository.find_by_id(pelicula_id)
        if not pelicula:
            raise ValueError(f"Pelicula con id {pelicula_id} no encontrada")
        return pelicula
                
    def registrarParaEspera(self, dni: int, pelicula_id: int) -> Union[ClienteDTO, MiembroDTO]:
        try:
            pelicula = self.repository.find_by_id(pelicula_id)
            if not pelicula:
                raise ValueError(f"Pelicula con id {pelicula_id} no encontrada")

            persona = self.repo_persona.find_by_dni(dni)
            if not persona:
                raise ValueError(f"Persona con DNI {dni} no encontrada")

            from services.entities.entidades import Cliente, Miembro
            from services.dto.PersonaDto import ClienteDTO, MiembroDTO

            if persona not in pelicula.personas_interesadas:
                pelicula.personas_interesadas.append(persona)
                self.repository.save(pelicula)
            else:
                print(f"{persona.nombre} ya está en la lista de espera para {pelicula.titulo}")

            if isinstance(persona, Cliente):
                return ClienteDTO.from_entity(persona)
            elif isinstance(persona, Miembro):
                return MiembroDTO.from_entity(persona)
            else:
                raise ValueError("Tipo de persona no soportado")

        except ValueError as e:
            print(f"Error al registrar para espera: {e}")
            return None