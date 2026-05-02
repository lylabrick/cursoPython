from constraint import Problem, AllDifferentConstraint

# ---------------------------------------------------------------------------
# DATOS DEL DOMINIO
# ---------------------------------------------------------------------------

MATERIAS = [
    "Algoritmos",
    "Estructuras",
    "Redes",
    "Bases de Datos",
    "Sistemas Operativos",
    "Compiladores",
]

DOCENTES = {
    "Algoritmos":        ["Garcia",   "Lopez"],
    "Estructuras":       ["Garcia",   "Perez"],
    "Redes":             ["Martinez", "Lopez"],
    "Bases de Datos":    ["Martinez", "Sanchez"],
    "Sistemas Operativos": ["Perez",  "Sanchez"],
    "Compiladores":      ["Lopez",    "Perez"],
}

# Aulas con su capacidad
AULAS = {
    "A101": 40,
    "A102": 30,
    "B201": 50,
    "B202": 25,
}

# Franjas horarias: (dia, hora)
FRANJAS = [
    ("Lunes",    "08:00"), ("Lunes",    "10:00"), ("Lunes",    "12:00"),
    ("Martes",   "08:00"), ("Martes",   "10:00"), ("Martes",   "12:00"),
    ("Miercoles","08:00"), ("Miercoles","10:00"), ("Miercoles","12:00"),
    ("Jueves",   "08:00"), ("Jueves",   "10:00"), ("Jueves",   "12:00"),
    ("Viernes",  "08:00"), ("Viernes",  "10:00"), ("Viernes",  "12:00"),
]

# Capacidad mínima requerida por materia
CAPACIDAD_REQUERIDA = {
    "Algoritmos":          45,
    "Estructuras":         28,
    "Redes":               30,
    "Bases de Datos":      40,
    "Sistemas Operativos": 22,
    "Compiladores":        25,
}

# Franjas que cada docente NO puede dar clase
RESTRICCIONES_DOCENTE = {
    "Garcia":   [("Lunes", "08:00"), ("Viernes", "12:00")],
    "Lopez":    [("Martes", "08:00")],
    "Martinez": [("Miercoles", "08:00"), ("Miercoles", "10:00")],
    "Perez":    [],
    "Sanchez":  [("Viernes", "08:00"), ("Viernes", "10:00")],
}

# ---------------------------------------------------------------------------
# CONSTRUCCIÓN DEL DOMINIO DE VALORES
# Cada variable es una materia.
# Cada valor posible es una tupla (docente, aula, franja)
# ya filtrada por restricciones individuales.
# ---------------------------------------------------------------------------

def dominio_para(materia: str) -> list[tuple]:
    valores = []
    for docente in DOCENTES[materia]:
        for aula, capacidad in AULAS.items():
            if capacidad < CAPACIDAD_REQUERIDA[materia]:
                continue                          # aula muy chica
            for franja in FRANJAS:
                if franja in RESTRICCIONES_DOCENTE[docente]:
                    continue                      # docente no disponible
                valores.append((docente, aula, franja))
    return valores


# ---------------------------------------------------------------------------
# RESTRICCIONES GLOBALES
# ---------------------------------------------------------------------------

def sin_conflicto_docente(*asignaciones):
    """Un docente no puede estar en dos materias en la misma franja."""
    ocupaciones = [(a[0], a[2]) for a in asignaciones]   # (docente, franja)
    return len(ocupaciones) == len(set(ocupaciones))


def sin_conflicto_aula(*asignaciones):
    """Un aula no puede tener dos materias en la misma franja."""
    ocupaciones = [(a[1], a[2]) for a in asignaciones]   # (aula, franja)
    return len(ocupaciones) == len(set(ocupaciones))


def sin_conflicto_franja(*asignaciones):
    """Dos materias no pueden compartir exactamente la misma franja."""
    franjas = [a[2] for a in asignaciones]
    return len(franjas) == len(set(franjas))


# ---------------------------------------------------------------------------
# RESOLUCIÓN
# ---------------------------------------------------------------------------

def resolver():
    problem = Problem()

    # Agregar variables con sus dominios
    for materia in MATERIAS:
        dom = dominio_para(materia)
        if not dom:
            print(f"[ERROR] Sin dominio válido para: {materia}")
            return None
        problem.addVariable(materia, dom)

    # Aplicar restricciones entre todos los pares de materias
    for i, m1 in enumerate(MATERIAS):
        for m2 in MATERIAS[i + 1:]:
            problem.addConstraint(
                lambda a, b: (
                    (a[0], a[2]) != (b[0], b[2]) and   # docente libre
                    (a[1], a[2]) != (b[1], b[2]) and   # aula libre
                    a[2] != b[2]                        # franja distinta
                ),
                (m1, m2),
            )

    print("Buscando solución...")
    solucion = problem.getSolution()
    return solucion


# ---------------------------------------------------------------------------
# PRESENTACIÓN
# ---------------------------------------------------------------------------

def mostrar(solucion: dict):
    if solucion is None:
        print("\n❌  No se encontró solución con las restricciones dadas.")
        return

    print("\n" + "═" * 64)
    print("  HORARIO ASIGNADO — Facultad de Informática")
    print("═" * 64)

    # Ordenar por día y hora
    orden_dia = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    orden_hora = ["08:00", "10:00", "12:00"]

    filas = []
    for materia, (docente, aula, franja) in solucion.items():
        dia, hora = franja
        filas.append((orden_dia.index(dia), orden_hora.index(hora),
                       dia, hora, materia, docente, aula))

    filas.sort(key=lambda x: (x[0], x[1]))

    print(f"\n{'Día':<12} {'Hora':<8} {'Materia':<22} {'Docente':<12} {'Aula':<6}")
    print("-" * 64)
    dia_actual = None
    for _, _, dia, hora, materia, docente, aula in filas:
        if dia != dia_actual:
            if dia_actual is not None:
                print()
            dia_actual = dia
        print(f"{dia:<12} {hora:<8} {materia:<22} {docente:<12} {aula:<6}")

    print("\n" + "═" * 64)

    # Resumen por docente
    print("\n  CARGA HORARIA POR DOCENTE")
    print("-" * 40)
    carga = {}
    for materia, (docente, aula, franja) in solucion.items():
        carga.setdefault(docente, []).append(f"{materia} ({franja[0]} {franja[1]})")
    for docente, clases in sorted(carga.items()):
        print(f"\n  {docente}:")
        for c in clases:
            print(f"    • {c}")

    # Resumen por aula
    print("\n\n  OCUPACIÓN DE AULAS")
    print("-" * 40)
    uso_aulas = {}
    for materia, (docente, aula, franja) in solucion.items():
        uso_aulas.setdefault(aula, []).append(
            f"{materia} — {franja[0]} {franja[1]} (cap. requerida: {CAPACIDAD_REQUERIDA[materia]})"
        )
    for aula, usos in sorted(uso_aulas.items()):
        print(f"\n  {aula} (cap. {AULAS[aula]}):")
        for u in usos:
            print(f"    • {u}")

    print("\n" + "═" * 64)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    solucion = resolver()
    mostrar(solucion)