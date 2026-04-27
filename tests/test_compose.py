# tests/test_compose.py
from practica3.compose import compose


def test_compose_equiv_anidado():
    f = lambda x: x + 1
    g = lambda x: x * 2
    h = lambda x: x - 3

    assert compose(f, g, h)(10) == f(g(h(10)))


def test_compose_una_funcion():
    f = lambda x: x * 10
    assert compose(f)(3) == 30


def test_compose_sin_funciones_es_identidad():
    assert compose()(123) == 123


def test_compose_puede_partir_con_args_y_kwargs_en_la_ultima():
    def h(x, y=0):
        return x + y

    g = lambda z: z * 2
    f = lambda z: z - 1

    assert compose(f, g, h)(10, y=5) == f(g(h(10, y=5)))