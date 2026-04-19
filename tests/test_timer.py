import unittest
from unittest.mock import patch
from utils import flatten_ejercicio1

class TestTimer(unittest.TestCase):
    """Tests para el decorador @timer"""

    def test_timer_no_altera_resultado(self):
        """El decorador timer no debe modificar el valor de retorno"""
        resultado = flatten_ejercicio1([[1, 2], [3]])
        self.assertEqual(resultado, [1, 2, 3])

    def test_timer_imprime_tiempo(self):
        with patch("builtins.print") as mock_print:
            flatten_ejercicio1([[1]])
            mensajes = [str(call) for call in mock_print.call_args_list]
            self.assertTrue(any("Tiempo de ejecución" in m for m in mensajes))

    def test_timer_imprime_nombre_funcion(self):
        with patch("builtins.print") as mock_print:
            flatten_ejercicio1([[1]])
            mensajes = [str(call) for call in mock_print.call_args_list]
            self.assertTrue(any("flatten_ejercicio1" in m for m in mensajes))