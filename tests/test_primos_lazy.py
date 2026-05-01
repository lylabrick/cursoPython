# tests/test_primos_lazy.py
from functools import reduce
from itertools import islice, takewhile

from practica3.primos_lazy import es_primo, primos


def test_es_primo_basicos():
    assert es_primo(2) is True
    assert es_primo(3) is True
    assert es_primo(4) is False
    assert es_primo(29) is True
    assert es_primo(1) is False
    assert es_primo(0) is False
    assert es_primo(-7) is False


def test_primeros_10_primos_lazy():
    assert list(islice(primos(), 10)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_primos_menores_50_con_takewhile():
    assert list(takewhile(lambda p: p < 50, primos())) == [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47
    ]


def test_suma_primeros_5_con_reduce():
    suma = reduce(lambda a, b: a + b, islice(primos(), 5), 0)
    assert suma == 28  # 2+3+5+7+11