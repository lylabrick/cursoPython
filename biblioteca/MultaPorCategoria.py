from biblioteca.EstrategiaMulta import EstrategiaMulta
from biblioteca.Libro import Libro

class MultaPorCategoria(EstrategiaMulta):
    TARIFAS = {
        "referencia": 200.0,
        "novela": 80.0,
        "ciencia": 150.0,
        "infantil": 50.0,
    }

    TARIFAS_DEFAULT = 100.0

    def calcular(self, dias_retraso: int, libro: "Libro") -> float:
        tarifa = self.TARIFAS.get(libro.categoria, self.TARIFAS_DEFAULT)
        return dias_retraso * tarifa
    
    def descripcion(self) -> str:
        return "Multa por categoría de libro"