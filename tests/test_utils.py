import unittest
from unittest.mock import patch
from utils import flatten_ejercicio1


class TestFlattenEjercicio1(unittest.TestCase):
    """Test para la función flatten_ejercicio1 (logica pura)"""

    def test_lista_plana(self):
        """Una lista que ya es plana no debería cambiar"""
        self.assertEqual(flatten_ejercicio1([1, 2, 3]), [1, 2, 3])

    def test_lista_anidad_un_niverl(self):
        self.assertEqual(flatten_ejercicio1([[1, 2], [3, 4]]), [1, 2, 3, 4])

    def test_lista_anidada_multiples_niveles(self):
        self.assertEqual(
            flatten_ejercicio1([[1, [2, 3]], [4, [5, [6]]]]), [1, 2, 3, 4, 5, 6]
        )

    def test_lista_vacia(self):
        self.assertEqual(flatten_ejercicio1([]), [])

    def test_lista_con_sublistas_vacias(self):
        self.assertEqual(flatten_ejercicio1([[], [], []]), [])

    def test_lista_con_strings(self):
        self.assertEqual(flatten_ejercicio1([["a", "b"], ["c"]]), ["a", "b", "c"])

    def test_lista_mixta_tipos(self):
        self.assertEqual(flatten_ejercicio1([[1, "dos"], [3.0]]), [1, "dos", 3.0])

    def test_elemento_unico(self):
        self.assertEqual(flatten_ejercicio1([[42]]), [42])

    def test_profundidad_alta(self):
        """lista muy anidada"""
        self.assertEqual(flatten_ejercicio1([[[[[1]]]]]), [1])

    def test_preserva_orden(self):
        """El orden de los elementos no debe cambiar"""
        self.assertEqual(flatten_ejercicio1([[3, 1], [4, 1, 5]]), [3, 1, 4, 1, 5])

    def test_valores_duplicados(self):
        self.assertEqual(flatten_ejercicio1([[1, 1], [1]]), [1, 1, 1])
