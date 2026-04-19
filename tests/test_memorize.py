import unittest
from unittest.mock import patch
from utils import flatten_ejercicio1


class TestMemorize(unittest.TestCase):
    """Tests para el decorador @memorize"""

    def setUp(self):
        flatten_ejercicio1.clear_cache()

    def test_cache_hit_devuelve_mismo_resultado(self):
        entrada = [[1, 2], [3, 4]]
        resultado1 = flatten_ejercicio1(entrada)
        resultado2 = flatten_ejercicio1(entrada)
        self.assertEqual(resultado1, resultado2)

    def test_cache_se_llena_en_primera_llamada(self):
        self.assertEqual(len(flatten_ejercicio1.cache), 0)
        flatten_ejercicio1([[1, 2]])
        self.assertEqual(len(flatten_ejercicio1.cache), 1)

    def test_cache_no_crece_en_llamadas_repetidas(self):
        entrada = [[1, 2], [3]]
        flatten_ejercicio1(entrada)
        flatten_ejercicio1(entrada)
        flatten_ejercicio1(entrada)
        self.assertEqual(len(flatten_ejercicio1.cache), 1)

    def test_distintas_entradas_generan_distintas_claves(self):
        flatten_ejercicio1([[1, 2]])
        flatten_ejercicio1([[3, 4]])
        self.assertEqual(len(flatten_ejercicio1.cache), 2)

    def test_clear_cache_vacia_el_cache(self):
        flatten_ejercicio1([[1, 2]])
        self.assertEqual(len(flatten_ejercicio1.cache), 1)
        flatten_ejercicio1.clear_cache()
        self.assertEqual(len(flatten_ejercicio1.cache), 0)

    def test_cache_hit_imprime_mensaje_correcto(self):
        entrada = [[1, 2]]
        flatten_ejercicio1(entrada) # primer llamado - CALCULADO

        with patch("builtins.print") as mock_print:
            flatten_ejercicio1(entrada) # segundo llamado - CACHE HIT
            # Verificar que alguno de los prints contiene "Cache hit"
            mensajes = [str(call) for call in mock_print.call_args_list]
            self.assertTrue(any("Cache hit" in m for m in mensajes))

    def test_primer_llamado_imprime_calculado(self):
        flatten_ejercicio1.clear_cache()
        with patch("builtins.print") as mock_print:
            flatten_ejercicio1([[99]])
            mensajes = [str(call) for call in mock_print.call_args_list]
            self.assertTrue(any("Calculado" in m for m in mensajes))
            
