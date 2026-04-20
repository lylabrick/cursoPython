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

    def test_tiempo_ejecucion_es_positivo(self):
        """Capturar el print del timer y verificar que el tiempo sea > 0"""
        tiempos_capturados = []

        def capturar_print(*args):
            texto = args[0] if args else ""
            if "Tiempo de ejecución" in texto:
                # extrae el número del string "Tiempo de ejecución de X: 0.000123 segundos"
                tiempo_str = texto.split(": ")[1].split(" ")[0]
                tiempos_capturados.append(float(tiempo_str))

        with patch("builtins.print", side_effect=capturar_print):
            flatten_ejercicio1.clear_cache()
            flatten_ejercicio1([[1, 2, 3]])

        print(f"tiempos capturados: {tiempos_capturados[0]:.6f}" )

        self.assertTrue(len(tiempos_capturados) > 0)
        self.assertGreater(tiempos_capturados[0], 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)