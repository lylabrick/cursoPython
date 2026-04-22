from biblioteca.EstrategiaMulta import EstrategiaMulta
from biblioteca.Libro import Libro

class MultaTarifaFija(EstrategiaMulta):

    def __init__(self, tarifa_fija: float = 500.0):
        self._tarifa_fija = tarifa_fija

    def calcular(self, dias_retraso: int, libro: "Libro") -> float:
        return self._tarifa_fija
    
    def descripcion(self) -> str:
        return f"Multa tarifa fija (${self.tarifa_fija})"