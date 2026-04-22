
from biblioteca.Libro import Libro
from biblioteca.EstrategiaMulta import EstrategiaMulta

class MultaPorDia(EstrategiaMulta):
    def __init__(self, tarifa_por_dia: float = 100.0):
        self._tarifa_por_dia = tarifa_por_dia

    def calcular(self, dias_retraso: int, libro: "Libro") -> float:
        return dias_retraso * self._tarifa_por_dia
    
    def descripcion(self) -> str:
        return f"Multa por dia (${self._tarifa_por_dia}/dia)"
    