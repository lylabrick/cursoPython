# practica3/currying.py
from __future__ import annotations

from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
R = TypeVar("R")


def curry3(fn: Callable[[A, B, C], R]) -> Callable[[A], Callable[[B], Callable[[C], R]]]:
    """
    Currying manual para una función de 3 argumentos:
    fn(a, b, c) -> curry3(fn)(a)(b)(c)
    """
    def f1(a: A) -> Callable[[B], Callable[[C], R]]:
        def f2(b: B) -> Callable[[C], R]:
            def f3(c: C) -> R:
                return fn(a, b, c)
            return f3
        return f2
    return f1


# Ejemplo práctico:
# calcular total con descuento e impuesto:
# total = precio * (1 - descuento_pct) * (1 + impuesto_pct)
def calcular_total(precio: float, descuento_pct: float, impuesto_pct: float) -> float:
    return precio * (1 - descuento_pct) * (1 + impuesto_pct)


if __name__ == "__main__":
    curried_total = curry3(calcular_total)

    # Configuración reutilizable para una tienda:
    # 10% descuento + 21% impuesto
    total_tienda = curried_total(0.0)  # <- solo para mostrar forma; abajo va uso correcto

    # Uso correcto por etapas:
    con_precio = curried_total(100.0)      # fija precio base
    con_descuento = con_precio(0.10)       # fija descuento
    resultado = con_descuento(0.21)        # aplica impuesto final

    print(resultado)  # 108.9

    # También en una sola línea:
    print(curried_total(100.0)(0.10)(0.21))  # 108.9