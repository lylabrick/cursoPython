import unittest
from datetime import date
from biblioteca.Socio import Socio

class TestSocio(unittest.TestCase):

    def setUp(self):
        self.socio = Socio("Laura", "laura@email.com", 1)

    def test_nombre(self):
        self.assertEqual(self.socio.nombre, "Laura")

    def test_email(self):
        self.assertEqual(self.socio.email, "laura@email.com")

    def test_numero_socio(self):
        self.assertEqual(self.socio.numero_socio, 1)

    def test_descripcion(self):
        self.assertEqual(self.socio.descripcion(), "Socio #1: Laura")

    def test_str(self):
        self.assertEqual(str(self.socio), "Socio #1: Laura")