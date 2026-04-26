# tests/test_biblioteca.py
from datetime import date

import pytest
from unittest.mock import MagicMock

from biblioteca.Autor import Autor
from biblioteca.Biblioteca import Biblioteca
from biblioteca.Libro import Libro
from biblioteca.Socio import Socio


class _FixedDate(date):
    @classmethod
    def today(cls):
        return cls(2026, 4, 25)


def test_biblioteca_agregar_libro_guarda_en_repo(monkeypatch):
    repo_libros = MagicMock()
    repo_socios = MagicMock()
    repo_prestamos = MagicMock()

    biblio = Biblioteca("Central", repo_libros, repo_socios, repo_prestamos)

    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")
    biblio.agregar_libro(libro)

    repo_libros.guardar.assert_called_once_with(libro)


def test_biblioteca_registrar_socio_guarda_en_repo():
    repo_libros = MagicMock()
    repo_socios = MagicMock()
    repo_prestamos = MagicMock()

    biblio = Biblioteca("Central", repo_libros, repo_socios, repo_prestamos)

    socio = Socio("Laura", "laura@email.com", 1)
    biblio.registrar_socio(socio)

    repo_socios.guardar.assert_called_once_with(socio)


def test_biblioteca_prestar_libro_ok_crea_prestamo_y_persiste(monkeypatch):
    import biblioteca.Biblioteca as biblioteca_mod

    monkeypatch.setattr(biblioteca_mod, "date", _FixedDate)

    repo_libros = MagicMock()
    repo_socios = MagicMock()
    repo_prestamos = MagicMock()

    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")
    socio = Socio("Laura", "laura@email.com", 1)

    repo_libros.buscar_por_isbn.return_value = libro
    repo_socios.buscar_por_numero.return_value = socio

    biblio = Biblioteca("Central", repo_libros, repo_socios, repo_prestamos)

    prestamo = biblio.prestar_libro("978-123", 1)

    assert prestamo is not None
    assert prestamo.libro is libro
    assert prestamo.socio is socio
    assert prestamo._fecha_inicio == date(2026, 4, 25)
    assert prestamo._fecha_limite == date(2026, 5, 2)
    assert libro.disponible is False

    repo_libros.buscar_por_isbn.assert_called_once_with("978-123")
    repo_socios.buscar_por_numero.assert_called_once_with(1)

    # se persiste el libro ya marcado como prestado
    assert repo_libros.guardar.call_count == 1
    repo_prestamos.guardar.assert_called_once()
    assert repo_prestamos.guardar.call_args[0][0] is prestamo


def test_biblioteca_prestar_libro_falla_si_no_hay_libro():
    repo_libros = MagicMock()
    repo_socios = MagicMock()
    repo_prestamos = MagicMock()

    repo_libros.buscar_por_isbn.return_value = None
    repo_socios.buscar_por_numero.return_value = Socio("Laura", "laura@email.com", 1)

    biblio = Biblioteca("Central", repo_libros, repo_socios, repo_prestamos)

    prestamo = biblio.prestar_libro("978-123", 1)

    assert prestamo is None
    repo_prestamos.guardar.assert_not_called()


def test_biblioteca_prestar_libro_falla_si_no_hay_socio():
    repo_libros = MagicMock()
    repo_socios = MagicMock()
    repo_prestamos = MagicMock()

    autor = Autor("Borges", "borges@email.com", "Argentina")
    repo_libros.buscar_por_isbn.return_value = Libro("Ficciones", autor, "978-123", "novela")
    repo_socios.buscar_por_numero.return_value = None

    biblio = Biblioteca("Central", repo_libros, repo_socios, repo_prestamos)

    prestamo = biblio.prestar_libro("978-123", 1)

    assert prestamo is None
    repo_prestamos.guardar.assert_not_called()


def test_biblioteca_prestar_libro_falla_si_no_disponible():
    repo_libros = MagicMock()
    repo_socios = MagicMock()
    repo_prestamos = MagicMock()

    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")
    libro.prestar()

    repo_libros.buscar_por_isbn.return_value = libro
    repo_socios.buscar_por_numero.return_value = Socio("Laura", "laura@email.com", 1)

    biblio = Biblioteca("Central", repo_libros, repo_socios, repo_prestamos)

    prestamo = biblio.prestar_libro("978-123", 1)

    assert prestamo is None
    repo_libros.guardar.assert_not_called()
    repo_prestamos.guardar.assert_not_called()


def test_biblioteca_devolver_libro_si_hay_prestamo(monkeypatch):
    repo_libros = MagicMock()
    repo_socios = MagicMock()
    repo_prestamos = MagicMock()

    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")
    socio = Socio("Laura", "laura@email.com", 1)

    # creamos un "prestamo" real para verificar efectos laterales
    from biblioteca.Prestamo import Prestamo

    libro.prestar()
    prestamo = Prestamo(libro, socio, date(2026, 4, 25), date(2026, 5, 2))

    # Biblioteca usa buscar_activo_por_isbn (así está en tu archivo)
    repo_prestamos.buscar_activo_por_isbn.return_value = prestamo

    biblio = Biblioteca("Central", repo_libros, repo_socios, repo_prestamos)

    biblio.devolver_libro("978-123")

    assert libro.disponible is True
    repo_libros.guardar.assert_called_once_with(libro)
    assert repo_prestamos.guardar.call_count == 1
    assert repo_prestamos.guardar.call_args[0][0] is prestamo


def test_biblioteca_devolver_libro_no_hace_nada_si_no_hay_prestamo():
    repo_libros = MagicMock()
    repo_socios = MagicMock()
    repo_prestamos = MagicMock()

    repo_prestamos.buscar_activo_por_isbn.return_value = None

    biblio = Biblioteca("Central", repo_libros, repo_socios, repo_prestamos)
    biblio.devolver_libro("978-123")

    repo_libros.guardar.assert_not_called()
    repo_prestamos.guardar.assert_not_called()


def test_biblioteca_libros_disponibles_filtra_por_disponible():
    repo_libros = MagicMock()
    repo_socios = MagicMock()
    repo_prestamos = MagicMock()

    autor = Autor("Borges", "borges@email.com", "Argentina")
    l1 = Libro("Ficciones", autor, "978-123", "novela")
    l2 = Libro("El Aleph", autor, "978-456", "cuento")
    l2.prestar()

    repo_libros.listar_todos.return_value = [l1, l2]

    biblio = Biblioteca("Central", repo_libros, repo_socios, repo_prestamos)
    disponibles = biblio.libros_disponibles()

    assert disponibles == [l1]


def test_str_biblioteca():
    repo_libros = MagicMock()
    repo_socios = MagicMock()
    repo_prestamos = MagicMock()
    biblio = Biblioteca("Central", repo_libros, repo_socios, repo_prestamos)
    assert str(biblio) == "Biblioteca 'Central'"