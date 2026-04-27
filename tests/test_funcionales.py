# tests/test_funcionales.py
import pytest

from practica3.funcionales import my_map, my_filter, my_reduce, _sentinel
from functools import reduce


def test_my_map_equiv_a_builtin_map_un_iterable():
    xs = [1, 2, 3, 4]
    assert list(my_map(lambda x: x * 2, xs)) == list(map(lambda x: x * 2, xs))


def test_my_map_equiv_a_builtin_map_varios_iterables_corta_al_mas_corto():
    a = [1, 2, 3]
    b = [10, 20]
    assert list(my_map(lambda x, y: x + y, a, b)) == list(map(lambda x, y: x + y, a, b))


def test_my_filter_con_func_equiv_a_builtin_filter():
    xs = [0, 1, 2, 3, 4, 5]
    assert list(my_filter(lambda x: x % 2 == 0, xs)) == list(filter(lambda x: x % 2 == 0, xs))


def test_my_filter_con_none_equiv_a_builtin_filter():
    xs = [0, 1, "", "a", [], [1], None, True, False]
    assert list(my_filter(None, xs)) == list(filter(None, xs))


def test_my_reduce_equiv_a_referencia_sin_initial():
    xs = [1, 2, 3, 4]
    f = lambda a, b: a + b
    assert my_reduce(f, xs) == reduce(f, xs)


def test_my_reduce_equiv_a_referencia_con_initial():
    xs = [1, 2, 3]
    f = lambda a, b: a * b
    assert my_reduce(f, xs, 10) == reduce(f, xs, 10)


def test_my_reduce_vacio_sin_initial_lanza_typeerror():
    with pytest.raises(TypeError):
        my_reduce(lambda a, b: a + b, [])