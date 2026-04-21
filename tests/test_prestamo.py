from datetime import date
import unittest
from biblioteca.Autor import Autor
from biblioteca.Socio import Socio
from biblioteca.Libro import Libro
from biblioteca.Prestamo import Prestamo
from biblioteca.Biblioteca import Biblioteca

class TestPrestamo(unittest.TestCase):

    def setUp(self):
        self.autor = Autor("Borges", "borges@email.com", "Argentina")
        self.libro = Libro("Ficciones", self.autor, "978-123")
        self.socio = Socio("Laura", "laura@email.com", 1)
        self.prestamo = Prestamo(self.libro, self.socio)

    def test_libro(self):
        self.assertEqual(self.prestamo.libro, self.libro)

    def test_socio(self):
        self.assertEqual(self.prestamo.socio, self.socio)

    def test_activo_por_defecto(self):
        self.assertTrue(self.prestamo.activo)

    def test_fecha_inicio_es_hoy(self):
        self.assertEqual(self.prestamo._fecha_inicio, date.today())

    def test_devolver(self):
        self.prestamo.devolver()
        self.assertFalse(self.prestamo.activo)

    def test_devolver_actualiza_libro(self):
        self.libro.prestar()
        self.prestamo.devolver()
        self.assertTrue(self.libro.disponible)

    def test_str_activo(self):
        self.assertIn("activo", str(self.prestamo))

    def test_str_devuelto(self):
        self.prestamo.devolver()
        self.assertIn("devuelto", str(self.prestamo))