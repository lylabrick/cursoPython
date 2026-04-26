# tests/test_repos_memoria.py
from datetime import date

from biblioteca.Autor import Autor
from biblioteca.Libro import Libro
from biblioteca.Prestamo import Prestamo
from biblioteca.Socio import Socio
from biblioteca.persistencia.implementacionenmemoria.RepositorioLibrosMemoria import (
    RepositorioLibrosMemoria,
)
from biblioteca.persistencia.implementacionenmemoria.RepositorioPrestamosMemoria import (
    RepositorioPrestamosMemoria,
)
from biblioteca.persistencia.implementacionenmemoria.RepositorioSociosMemoria import (
    RepositorioSociosMemoria,
)


def test_repo_libros_memoria_crud_basico():
    repo = RepositorioLibrosMemoria()
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")

    assert repo.buscar_por_isbn("978-123") is None

    repo.guardar(libro)
    assert repo.buscar_por_isbn("978-123") is libro
    assert repo.listar_todos() == [libro]

    repo.eliminar("978-123")
    assert repo.buscar_por_isbn("978-123") is None
    assert repo.listar_todos() == []


def test_repo_socios_memoria_crud_basico():
    repo = RepositorioSociosMemoria()
    s1 = Socio("Laura", "laura@email.com", 1)
    s2 = Socio("Pedro", "pedro@email.com", 2)

    assert repo.buscar_por_numero(1) is None

    repo.guardar(s1)
    repo.guardar(s2)

    assert repo.buscar_por_numero(1) is s1
    assert repo.buscar_por_numero(2) is s2
    assert sorted([s.numero_socio for s in repo.listar_todos()]) == [1, 2]


def test_repo_prestamos_memoria_listar_archivos_devuelve_solo_activos():
    repo = RepositorioPrestamosMemoria()

    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro1 = Libro("Ficciones", autor, "978-123", "novela")
    libro2 = Libro("El Aleph", autor, "978-456", "cuento")
    socio = Socio("Laura", "laura@email.com", 1)

    libro1.prestar()
    libro2.prestar()

    p1 = Prestamo(libro1, socio, date(2026, 4, 25), date(2026, 5, 2))
    p2 = Prestamo(libro2, socio, date(2026, 4, 25), date(2026, 5, 2))
    p2.devolver(date(2026, 4, 26))

    repo.guardar(p1)
    repo.guardar(p2)

    activos = repo.listar_archivos()
    assert activos == [p1]

    assert repo.buscar_archivo_por_isbn("978-123") is p1
    assert repo.buscar_archivo_por_isbn("978-456") is None