# practica3/ventas.py
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class Venta:
    fecha: date
    producto: str
    cantidad: int
    precio_unitario: Decimal

    @property
    def monto(self) -> Decimal:
        return Decimal(self.cantidad) * self.precio_unitario


def _parse_decimal(s: str) -> Decimal:
    s = (s or "").strip()
    try:
        return Decimal(s)
    except InvalidOperation as e:
        raise ValueError(f"precio inválido: {s!r}") from e


def _parse_int(s: str) -> int:
    s = (s or "").strip()
    try:
        return int(s)
    except ValueError as e:
        raise ValueError(f"cantidad inválida: {s!r}") from e


def _parse_date(s: str) -> date:
    s = (s or "").strip()
    try:
        y, m, d = (int(p) for p in s.split("-"))
        return date(y, m, d)
    except Exception as e:
        raise ValueError(f"fecha inválida: {s!r}") from e


def parsear_ventas_csv(csv_text: str) -> tuple[Venta, ...]:
    """
    Entrada: texto CSV completo (inmutable conceptualmente: no muta el string).
    Salida: tupla inmutable de Venta (frozen dataclass).
    """
    reader = csv.DictReader(csv_text.splitlines())
    if reader.fieldnames is None:
        return ()

    required = {"fecha", "producto", "cantidad", "precio_unitario"}
    fset = {fn.strip() for fn in reader.fieldnames}
    missing = required - fset
    if missing:
        raise ValueError(f"Faltan columnas en el CSV: {sorted(missing)}")

    ventas: list[Venta] = []
    for row in reader:
        ventas.append(
            Venta(
                fecha=_parse_date(row["fecha"]),
                producto=(row["producto"] or "").strip(),
                cantidad=_parse_int(row["cantidad"]),
                precio_unitario=_parse_decimal(row["precio_unitario"]),
            )
        )
    return tuple(ventas)


def total_vendido_por_producto(ventas: Sequence[Venta]) -> tuple[tuple[str, Decimal], ...]:
    """
    Devuelve tupla de pares (producto, total) sin mutar `ventas`.
    """
    totales: dict[str, Decimal] = {}
    for v in ventas:
        # construimos un dict nuevo por fila sería caro; acá acumulamos en dict local
        # (no muta la entrada). Si querés “cero mutación interna”, se puede con reduce.
        totales[v.producto] = totales.get(v.producto, Decimal("0")) + v.monto

    items = tuple(sorted(totales.items(), key=lambda kv: kv[0]))
    return items


def top_productos_por_total(
    totales: Mapping[str, Decimal],
    n: int = 5,
) -> tuple[tuple[str, Decimal], ...]:
    """
    Top N por total vendido (monto).
    """
    ranked = tuple(sorted(totales.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
    return ranked[:n]


def promedio_venta_diaria(ventas: Sequence[Venta]) -> Decimal:
    """
    Promedio = (suma de montos) / (días distintos con al menos una venta).
    Si no hay ventas => 0.
    """
    if not ventas:
        return Decimal("0")

    total = sum((v.monto for v in ventas), Decimal("0"))
    dias = {v.fecha for v in ventas}
    return total / Decimal(len(dias))


def resumen_ventas(csv_text: str) -> dict[str, object]:
    """
    Orquestación pura: csv_text -> resultados.
    """
    ventas = parsear_ventas_csv(csv_text)
    totales_map = dict(total_vendido_por_producto(ventas))  # dict solo para reutilizar top_*; podés evitarlo
    top5 = top_productos_por_total(totales_map, 5)
    prom = promedio_venta_diaria(ventas)

    return {
        "ventas": ventas,
        "total_por_producto": tuple(totales_map.items()),  # inmutable-ish
        "top5_productos": top5,
        "promedio_venta_diaria": prom,
    }


def leer_archivo_y_resumen(ruta_csv: str) -> dict[str, object]:
    """
    NO es pura (I/O). Úsala en main/scripts; testeá `resumen_ventas` con strings.
    """
    with open(ruta_csv, "r", encoding="utf-8") as f:
        return resumen_ventas(f.read())