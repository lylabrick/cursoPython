from biblioteca.EstrategiaMulta import EstrategiaMulta
from biblioteca.Libro import Libro

class MultaEscalonada(EstrategiaMulta):
    """Aumenta la tarifa por dia según el rango de días de retraso"""
    ESCALONES = [
        (3,  50.0),   # hasta 3 días  → $50/día
        (7,  100.0),  # hasta 7 días  → $100/día
        (14, 200.0),  # hasta 14 días → $200/día
    ]
    TARIFA_MAXIMA = 300.0

    def calcular(self, dias_retraso: int, libro: "Libro") -> float:
        for limite, tarifa in self.ESCALONES:
            if dias_retraso <= limite:
                return dias_retraso * tarifa
        return dias_retraso * self.TARIFA_MAXIMA
    
    def descripcion(self) -> str:
        return "Multa escalonada según dias de retraso"


