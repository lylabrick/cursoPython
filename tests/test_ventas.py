# tests/test_ventas.py
from decimal import Decimal

from practica3.ventas import resumen_ventas

def test_resumen_totales_top5_y_promedio_diario():
    csv_text = "\n".join(
        [
            "fecha,producto,cantidad,precio_unitario",
            "2026-04-01,A,2,10.00",
            "2026-04-01,B,1,5.00",
            "2026-04-02,A,1,10.00",
            "2026-04-02,C,3,2.00",
            "2026-04-03,B,2,5.00",
            "2026-04-03,D,1,100.00",
            "2026-04-04,E,1,1.00",
        ]
    )

    r = resumen_ventas(csv_text)

    totales = dict(r["total_por_producto"])
    assert totales["A"] == Decimal("30.00")  # 20 + 10
    assert totales["B"] == Decimal("15.00")  # 5 + 10
    assert totales["C"] == Decimal("6.00")
    assert totales["D"] == Decimal("100.00")
    assert totales["E"] == Decimal("1.00")

    top5 = list(r["top5_productos"])
    assert [p for p, _ in top5] == ["D", "A", "B", "C", "E"]

    # 4 días distintos: 2026-04-01..04-04
    assert r["promedio_venta_diaria"] == (Decimal("152.00") / Decimal("4"))