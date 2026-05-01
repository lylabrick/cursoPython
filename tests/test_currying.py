# tests/test_currying.py
from practica3.currying import curry3, calcular_total


def test_curry3_equivalente_a_llamada_directa():
    curried = curry3(calcular_total)

    directo = calcular_total(100.0, 0.10, 0.21)
    curried_result = curried(100.0)(0.10)(0.21)

    assert curried_result == directo
    assert round(curried_result, 2) == 108.90


def test_curry3_reutiliza_argumentos_parciales():
    curried = curry3(calcular_total)

    # fijamos descuento e impuesto para distintos precios
    def total_con_reglas(precio: float):
        return curried(precio)(0.15)(0.21)

    assert round(total_con_reglas(200.0), 2) == round(calcular_total(200.0, 0.15, 0.21), 2)
    assert round(total_con_reglas(80.0), 2) == round(calcular_total(80.0, 0.15, 0.21), 2)
    assert round(total_con_reglas(90.0), 2) == round(calcular_total(90.0, 0.15, 0.21), 2)