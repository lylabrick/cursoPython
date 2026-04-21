import unittest
from biblioteca.Autor import Autor

class TestAutor(unittest.TestCase):

    def setUp(self):
        self.autor = Autor("Borges", "borges@gmail.com", "Argentina")

    def test_nombre(self):
        self.assertEqual(self.autor.nombre, "Borges")

    def test_email(self):
        self.assertEqual(self.autor.email, "borges@gmail.com")

    def test_nacionalidad(self):
        self.assertEqual(self.autor.nacionalidad, "Argentina")

    def test_descripcion(self):
        self.assertEqual(self.autor.descripcion(), "Autor: Borges (Argentina)")
    
    def test_str(self):
        self.assertEqual(str(self.autor), "Autor: Borges (Argentina)")
    