from datetime import date

from biblioteca.Autor import Autor
from biblioteca.Libro import Libro
from biblioteca.Prestamo import Prestamo
from biblioteca.Socio import Socio


def test_prestamo_libro_y_socio():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123")
    socio = Socio("Laura", "laura@email.com", 1)

    prestamo = Prestamo(libro, socio, date(2026, 4, 25), date(2026, 5, 2))

    assert prestamo.libro is libro
    assert prestamo.socio is socio


def test_prestamo_activo_por_defecto():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123")
    socio = Socio("Laura", "laura@email.com", 1)

    prestamo = Prestamo(libro, socio, date(2026, 4, 25), date(2026, 5, 2))

    assert prestamo.activo is True


def test_devolver_setea_fecha_y_devuelve_libro():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123")
    socio = Socio("Laura", "laura@email.com", 1)

    libro.prestar()
    assert libro.disponible is False

    prestamo = Prestamo(libro, socio, date(2026, 4, 25), date(2026, 5, 2))
    prestamo.devolver(date(2026, 4, 26))

    assert prestamo.activo is False
    assert prestamo._fecha_devolucion == date(2026, 4, 26)
    assert libro.disponible is True


def test_str_activo_y_devuelto():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123")
    socio = Socio("Laura", "laura@email.com", 1)

    prestamo = Prestamo(libro, socio, date(2026, 4, 25), date(2026, 5, 2))
    assert "activo" in str(prestamo)

    prestamo.devolver(date(2026, 4, 26))
    s = str(prestamo)
    assert "devuelto" in s
    assert "2026-04-26" in s