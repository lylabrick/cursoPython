# practica3/primos_lazy.py
from __future__ import annotations

from functools import reduce
from itertools import count, islice, takewhile
from math import isqrt
from typing import Iterator


def es_primo(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    limite = isqrt(n)
    # usamos reduce (functools) para combinar chequeos de divisibilidad
    return reduce(
        lambda acc, d: acc and (n % d != 0),
        range(3, limite + 1, 2),
        True,
    )


def primos() -> Iterator[int]:
    """
    Generador infinito y lazy de números primos.
    No guarda todos los primos en memoria.
    """
    for n in count(2):  # itertools.count -> secuencia infinita
        if es_primo(n):
            yield n


if __name__ == "__main__":
    # primeros 15 primos (lazy: islice corta sin materializar infinito)
    primeros_15 = list(islice(primos(), 15))
    print("Primeros 15:", primeros_15)

    # primos menores a 100 (lazy: takewhile corta en cuanto no cumple)
    menores_100 = list(takewhile(lambda p: p < 100, primos()))
    print("Menores a 100:", menores_100)

    # ejemplo de composición lazy adicional:
    # suma de los primeros 20 primos
    suma_20 = reduce(lambda a, b: a + b, islice(primos(), 20), 0)
    print("Suma primeros 20:", suma_20)