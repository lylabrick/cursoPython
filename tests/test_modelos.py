# tests/test_modelos.py
from datetime import date

from biblioteca.Autor import Autor
from biblioteca.Libro import Libro
from biblioteca.Prestamo import Prestamo
from biblioteca.Socio import Socio


def test_libro_prestar_y_devolver_cambia_disponible():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")

    assert libro.disponible is True
    libro.prestar()
    assert libro.disponible is False
    libro.devolver()
    assert libro.disponible is True


def test_str_libro():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")
    assert str(libro) == "'Ficciones' [novela]"


def test_descripcion_autor_y_socio_y_str_persona():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    socio = Socio("Laura", "laura@email.com", 1)

    assert autor.descripcion() == "Autor: Borges (Argentina)"
    assert str(autor) == "Autor: Borges (Argentina)"

    assert socio.descripcion() == "Socio #1: Laura"
    assert str(socio) == "Socio #1: Laura"


def test_prestamo_activo_y_devolver():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")
    socio = Socio("Laura", "laura@email.com", 1)

    libro.prestar()
    assert libro.disponible is False

    p = Prestamo(libro, socio, date(2026, 4, 25), date(2026, 5, 2))
    assert p.activo is True
    assert "activo" in str(p)

    p.devolver(date(2026, 4, 26))
    assert p.activo is False
    assert libro.disponible is True
    assert "devuelto el 2026-04-26" in str(p)