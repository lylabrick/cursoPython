from services.serviciosPelicula import ServicioPelicula
from services.entities.entidades import Pelicula, Persona, Alquiler
from repository.PersonaRepository import PersonaRepository
from repository.PeliculaRepository import PeliculaRepository
from services.dto.PeliculaDto import PeliculaDTO
from services.dto.AlquilerDto import AlquilerDTO
from services.dto.PeliculaDto import PeliculaDTO

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
    
        pelicula.notificar_observadores(pelicula.titulo)

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
        
        # 3. Buscar al cliente por DNI
        cliente = self.repo_persona.find_by_dni(dni)
        if not cliente:
            raise ValueError(f"Cliente con DNI {dni} no encontrado")
            
        # 4. Cambiar el estado de la película
        pelicula.estado = "Alquilada"

        # 5. Calcular cobro dinámicamente usando el patrón Strategy que creamos en tu Entidad
        precio_base = pelicula.precio  # El costo estándar del alquiler
        precio_final = cliente.calcular_cobro(precio_base)
        print(f"\n--- TICKET DE COBRO ---")
        print(f"Cliente: {cliente.nombre} (Tipo: {cliente.__class__.__name__})")
        print(f"Película: {pelicula.titulo}")
        print(f"Total Cobrado: ${precio_final} (Estrategia: {cliente.estrategia.__class__.__name__})")
        print(f"-----------------------\n")

        # 6. Crear el registro en la tabla Alquiler
        from datetime import date
        from services.entities.entidades import Alquiler
        from services.dto.AlquilerDto import AlquilerDTO
        
        nuevo_alquiler = Alquiler(
            pelicula=pelicula,
            cliente=cliente,
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
        try: 
            pelicula = self.repository.find_by_id(pelicula_id)
            if not pelicula:
                raise ValueError(f"Pelicula con id {pelicula_id} no encontrada")
            return pelicula
        except ValueError as e:
            print(f"Error al buscar película por id: {e}")
            return None
            
    def registrarParaEspera(self, dni: int, pelicula_id: int) -> None:
        try:
            # 1. Buscar la película
            pelicula = self.repository.find_by_id(pelicula_id)
            if not pelicula:
                raise ValueError(f"Pelicula con id {pelicula_id} no encontrada")

            # 2. Buscar la persona por DNI
            # (Necesitarás acceso al repositorio de personas o llamar a un método de persona)
            # Asumiendo que `self.repo_persona` existe o pasamos el repo de personas
            cliente = self.repo_persona.find_by_dni(dni)
            if not cliente:
                raise ValueError(f"Cliente con DNI {dni} no encontrado")

            # 3. Agregar a la lista de interesados
            # Verificamos si ya está para evitar duplicados (opcional, pero buena práctica)
            if cliente not in pelicula.interesados:
                pelicula.interesados.append(cliente)
                self.repository.save(pelicula) # Guardar cambios en la película
            else:
                print(f"El cliente {cliente.nombre} ya está en la lista de espera para {pelicula.titulo}")

            return ClienteDTO.from_entity(cliente) # O un mensaje de éxito
        
        except ValueError as e:
            print(f"Error al registrar para espera: {e}")
            return None