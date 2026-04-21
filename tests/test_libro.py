import unittest
from biblioteca.Autor import Autor
from biblioteca.Libro import Libro

class TestLibro(unittest.TestCase):

    def setUp(self):
        self.autor = Autor("Borges", "borges@email.com", "Argentina")
        self.libro = Libro("Ficciones", self.autor, "978-123")

    def test_titulo(self):
        self.assertEqual(self.libro.titulo, "Ficciones")

    def test_autor(self):
        self.assertEqual(self.libro.autor, self.autor)

    def test_isbn(self):
        self.assertEqual(self.libro.isbn, "978-123")

    def test_disponible_por_defecto(self):
        self.assertTrue(self.libro.disponible)

    def test_prestar(self):
        self.libro.prestar()
        self.assertFalse(self.libro.disponible)

    def test_devolver(self):
        self.libro.prestar()
        self.libro.devolver()
        self.assertTrue(self.libro.disponible)

    def test_str_disponible(self):
        self.assertIn("disponible", str(self.libro))

    def test_str_prestado(self):
        self.libro.prestar()
        self.assertIn("prestado", str(self.libro))