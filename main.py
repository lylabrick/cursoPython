from biblioteca.persistencia.implementacionenjson.RepositorioSociosJson import RepositorioSociosJson
from biblioteca.persistencia.implementacionenjson.RepositorioPrestamosJson import RepositorioPrestamosJson
from biblioteca.persistencia.implementacionenjson.RepositorioLibrosJson import RepositorioLibrosJson
from biblioteca.persistencia.implementacionenmemoria.RepositorioLibrosMemoria import RepositorioLibrosMemoria
from biblioteca.persistencia.implementacionenmemoria.RepositorioSociosMemoria import RepositorioSociosMemoria
from biblioteca.persistencia.implementacionenmemoria.RepositorioPrestamosMemoria import RepositorioPrestamosMemoria
from biblioteca.Biblioteca import Biblioteca
from biblioteca.Autor import Autor
from biblioteca.Libro import Libro
from biblioteca.Socio import Socio


autor = Autor("Borges", "borges@email.com", "Argentina")
libro = Libro("Ficciones", autor, "978-123", "novela")
socio = Socio("Laura", "laura@email.com", 1)

# ── con memoria (sin tocar lógica de negocio)
biblioteca_memoria = Biblioteca(
    "Biblioteca Central",
    RepositorioLibrosMemoria(),
    RepositorioSociosMemoria(),
    RepositorioPrestamosMemoria()
)

biblioteca_memoria.agregar_libro(libro)
biblioteca_memoria.registrar_socio(socio)
prestamo = biblioteca_memoria.prestar_libro("978-123", 1)
print(prestamo)
# → Préstamo de 'Ficciones' a Laura [activo]

# ── con JSON (misma lógica de negocio, distinta persistencia)
biblioteca_json = Biblioteca(
    "Biblioteca Central",
    RepositorioLibrosJson("libros.json"),
    RepositorioSociosJson("socios.json"),
    RepositorioPrestamosJson("prestamos.json")
)

biblioteca_json.agregar_libro(libro)
biblioteca_json.registrar_socio(socio)
prestamo = biblioteca_json.prestar_libro("978-123", 1)
print(prestamo)