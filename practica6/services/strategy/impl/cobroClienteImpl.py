from services.strategy.EstrategiaCobro import EstrategiaCobro

class CobroCliente(EstrategiaCobro):
    """Clientes pagan el precio completo."""

    def calcular_precio(self, precio_base: float) -> float:
        return precio_base
