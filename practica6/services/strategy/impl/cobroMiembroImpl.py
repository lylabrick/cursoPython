from services.strategy.EstrategiaCobro import EstrategiaCobro
from services.entities.entidades import Miembro

class CobroMiembro(EstrategiaCobro):
    """Miembros pagan con descuento según su atributo descuento."""

    def __init__(self, miembro: Miembro):
        self.miembro = miembro

    def calcular_precio(self, precio_base: float) -> float:
        descuento = self.miembro.descuento  # ej: 0.20 = 20% de descuento
        return precio_base * (1 - descuento)
