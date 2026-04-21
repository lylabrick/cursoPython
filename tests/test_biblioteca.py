import unittest

from biblioteca.Autor import Autor
from biblioteca.Biblioteca import Biblioteca
from biblioteca.Socio import Socio
from biblioteca.Libro import Libro 

class TestBiblioteca(unittest.TestCase):

    def setUp(self):
        self.biblioteca = Biblioteca("Biblioteca Central")
        self.autor = Autor("Borges", "borges@email.com", "Argentina")
        self.socio = Socio("Laura", "laura@email.com", 1)
        self.libro = Libro("Ficciones", self.autor, "978-123")
        self.biblioteca.agregar_libro(self.libro)
        self.biblioteca.registrar_socio(self.socio)

    def test_agregar_libro(self):
        self.assertIn(self.libro, self.biblioteca._libros)

    def test_registrar_socio(self):
        self.assertIn(self.socio, self.biblioteca._socios)
    
    def test_prestar_libro(self):
        prestamo = self.biblioteca.prestar_libro("978-123", self.socio)
        self.assertIsNotNone(prestamo)
        self.assertFalse(self.libro.disponible)

    def test_prestar_libro_no_disponible(self):
        self.biblioteca.prestar_libro("978-123", self.socio)
        prestamo2 = self.biblioteca.prestar_libro("978-123", self.socio)
        self.assertIsNone(prestamo2)

    def test_prestar_libro_isbn_inexistente(self):
        prestamo = self.biblioteca.prestar_libro("000-000", self.socio)
        self.assertIsNone(prestamo)

    def test_devolver_libro(self):
        self.biblioteca.prestar_libro("978-123", self.socio)
        self.biblioteca.devolver_libro("978-123")
        self.assertTrue(self.libro.disponible)

    def test_libros_disponibles(self):
        self.assertEqual(len(self.biblioteca.libros_disponibles()), 1)
        self.biblioteca.prestar_libro("978-123", self.socio)
        self.assertEqual(len(self.biblioteca.libros_disponibles()), 0)

    def test_prestamos_activos(self):
        self.assertEqual(len(self.biblioteca.prestamos_activos()), 0)
        self.biblioteca.prestar_libro("978-123", self.socio)
        self.assertEqual(len(self.biblioteca.prestamos_activos()), 1)

    def test_prestamos_activos_tras_devolucion(self):
        self.biblioteca.prestar_libro("978-123", self.socio)
        self.biblioteca.devolver_libro("978-123")
        self.assertEqual(len(self.biblioteca.prestamos_activos()), 0)

    def test_str(self):
        self.assertIn("Biblioteca Central", str(self.biblioteca))


if __name__ == "__main__":
    unittest.main()