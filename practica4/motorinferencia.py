"""
Motor de Inferencia - Forward Chaining
======================================
Implementación de un motor de inferencia simple desde cero
usando diccionarios y conjuntos. Soporta:
  - Base de hechos (facts)
  - Base de reglas (rules) con múltiples premisas y conclusiones
  - Encadenamiento hacia adelante (forward chaining)
  - Consultas simples y explicación del razonamiento (trace)
"""


# ---------------------------------------------------------------------------
# ESTRUCTURAS DE DATOS
# ---------------------------------------------------------------------------

class Regla:
    """
    Representa una regla de producción de la forma:
        SI premisas ENTONCES conclusiones
    """

    def __init__(self, nombre: str, premisas: list[str], conclusiones: list[str]):
        self.nombre = nombre
        self.premisas = set(premisas)      # condiciones necesarias
        self.conclusiones = set(conclusiones)  # hechos que se derivan

    def __repr__(self):
        premisas_str = " ∧ ".join(sorted(self.premisas))
        concls_str = " ∧ ".join(sorted(self.conclusiones))
        return f"[{self.nombre}] SI {premisas_str} → ENTONCES {concls_str}"


class BaseDeConocimiento:
    """
    Contiene la base de hechos y la base de reglas.
    Provee métodos para cargar hechos, cargar reglas y consultar.
    """

    def __init__(self):
        self.hechos: set[str] = set()          # hechos conocidos
        self.reglas: list[Regla] = []          # lista de reglas
        self._historial: list[dict] = []       # registro de inferencias realizadas

    # ------------------------------------------------------------------
    # Carga de conocimiento
    # ------------------------------------------------------------------

    def agregar_hecho(self, *hechos: str):
        """Agrega uno o más hechos a la base de conocimiento."""
        for h in hechos:
            h = h.strip().lower()
            self.hechos.add(h)

    def agregar_regla(self, nombre: str, premisas: list[str], conclusiones: list[str]):
        """Agrega una regla a la base de conocimiento."""
        premisas_norm = [p.strip().lower() for p in premisas]
        conclusiones_norm = [c.strip().lower() for c in conclusiones]
        self.reglas.append(Regla(nombre, premisas_norm, conclusiones_norm))

    def cargar_base(self, hechos_iniciales: list[str], reglas_def: list[dict]):
        """
        Carga masiva de hechos y reglas.

        reglas_def es una lista de dicts con la forma:
            {"nombre": str, "si": [str, ...], "entonces": [str, ...]}
        """
        self.agregar_hecho(*hechos_iniciales)
        for r in reglas_def:
            self.agregar_regla(r["nombre"], r["si"], r["entonces"])

    # ------------------------------------------------------------------
    # Motor de inferencia — Forward Chaining
    # ------------------------------------------------------------------

    def inferir(self, verbose: bool = False) -> set[str]:
        """
        Ejecuta el encadenamiento hacia adelante hasta que no se puedan
        derivar nuevos hechos (punto fijo).

        Retorna el conjunto de todos los hechos conocidos al terminar.
        Si verbose=True, imprime cada paso del razonamiento.
        """
        self._historial.clear()
        hechos_actuales = set(self.hechos)   # copia de trabajo
        reglas_pendientes = list(self.reglas)  # reglas aún no disparadas

        if verbose:
            print("=" * 60)
            print("INICIO DEL ENCADENAMIENTO HACIA ADELANTE")
            print("=" * 60)
            print(f"Hechos iniciales: {sorted(hechos_actuales)}\n")

        iteracion = 0
        while True:
            iteracion += 1
            nuevos_hechos: set[str] = set()
            reglas_no_disparadas = []

            for regla in reglas_pendientes:
                # ¿Todas las premisas están satisfechas?
                if regla.premisas.issubset(hechos_actuales):
                    # Calcular conclusiones realmente nuevas
                    inferidos = regla.conclusiones - hechos_actuales
                    if inferidos:
                        nuevos_hechos |= inferidos
                        entrada_historial = {
                            "iteracion": iteracion,
                            "regla": regla.nombre,
                            "premisas_usadas": sorted(regla.premisas),
                            "hechos_nuevos": sorted(inferidos),
                        }
                        self._historial.append(entrada_historial)

                        if verbose:
                            print(f"  Iteración {iteracion} — Regla disparada: {regla.nombre}")
                            print(f"    Premisas: {sorted(regla.premisas)}")
                            print(f"    Nuevos hechos: {sorted(inferidos)}")
                    # La regla ya se disparó; no la volvemos a evaluar
                else:
                    reglas_no_disparadas.append(regla)

            if not nuevos_hechos:
                # Punto fijo alcanzado
                if verbose:
                    print(f"\nPunto fijo alcanzado en iteración {iteracion}.")
                    print(f"Total de hechos: {len(hechos_actuales)}")
                    print("=" * 60)
                break

            hechos_actuales |= nuevos_hechos
            reglas_pendientes = reglas_no_disparadas

        # Actualizar la base con todos los hechos derivados
        self.hechos = hechos_actuales
        return hechos_actuales

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def consultar(self, hecho: str) -> bool:
        """
        Consulta si un hecho puede ser derivado.
        Ejecuta la inferencia completa antes de responder.
        """
        self.inferir()
        return hecho.strip().lower() in self.hechos

    def explicar(self, hecho: str) -> str:
        """
        Explica cómo se llegó a un hecho mostrando la cadena
        de reglas que lo derivaron.
        Llama a inferir() solo si el historial está vacío.
        """
        hecho = hecho.strip().lower()
        if not self._historial:
            self.inferir()

        if hecho not in self.hechos:
            return f"El hecho '{hecho}' NO puede ser derivado con el conocimiento actual."

        # Buscar en el historial las reglas que lo produjeron
        cadena = []
        for entrada in self._historial:
            if hecho in entrada["hechos_nuevos"]:
                cadena.append(entrada)

        if not cadena:
            return f"'{hecho}' es un hecho inicial (no derivado por ninguna regla)."

        lineas = [f"El hecho '{hecho}' fue derivado mediante:"]
        for paso in cadena:
            lineas.append(
                f"  • Regla '{paso['regla']}' "
                f"(premisas: {paso['premisas_usadas']}) "
                f"en iteración {paso['iteracion']}"
            )
        return "\n".join(lineas)

    def listar_hechos(self) -> list[str]:
        """Retorna la lista de todos los hechos conocidos, ordenada."""
        return sorted(self.hechos)

    def listar_reglas(self) -> list[str]:
        """Retorna la lista de todas las reglas registradas."""
        return [str(r) for r in self.reglas]

    def historial(self) -> list[dict]:
        """Retorna el historial de inferencias de la última ejecución."""
        return list(self._historial)

    def resetear_hechos(self, hechos_iniciales: list[str]):
        """Reinicia la base de hechos (mantiene las reglas)."""
        self.hechos = {h.strip().lower() for h in hechos_iniciales}
        self._historial.clear()


# ---------------------------------------------------------------------------
# BASE DE CONOCIMIENTO DE EJEMPLO — Diagnóstico de animales
# ---------------------------------------------------------------------------

def construir_base_animales() -> BaseDeConocimiento:
    bc = BaseDeConocimiento()

    reglas = [
        {
            "nombre": "R1 - tiene_pelo → mamifero",
            "si": ["tiene_pelo"],
            "entonces": ["mamifero"],
        },
        {
            "nombre": "R2 - da_leche → mamifero",
            "si": ["da_leche"],
            "entonces": ["mamifero"],
        },
        {
            "nombre": "R3 - tiene_plumas → ave",
            "si": ["tiene_plumas"],
            "entonces": ["ave"],
        },
        {
            "nombre": "R4 - vuela + pone_huevos → ave",
            "si": ["vuela", "pone_huevos"],
            "entonces": ["ave"],
        },
        {
            "nombre": "R5 - mamifero + come_carne → carnivoro",
            "si": ["mamifero", "come_carne"],
            "entonces": ["carnivoro"],
        },
        {
            "nombre": "R6 - mamifero + tiene_dientes_afilados + ojos_al_frente → carnivoro",
            "si": ["mamifero", "tiene_dientes_afilados", "ojos_al_frente"],
            "entonces": ["carnivoro"],
        },
        {
            "nombre": "R7 - mamifero + tiene_pezunas → ungulado",
            "si": ["mamifero", "tiene_pezunas"],
            "entonces": ["ungulado"],
        },
        {
            "nombre": "R8 - mamifero + rumia → ungulado",
            "si": ["mamifero", "rumia"],
            "entonces": ["ungulado"],
        },
        {
            "nombre": "R9 - carnivoro + color_leonado + manchas_oscuras → guepardo",
            "si": ["carnivoro", "color_leonado", "manchas_oscuras"],
            "entonces": ["guepardo"],
        },
        {
            "nombre": "R10 - carnivoro + color_leonado + rayas_negras → tigre",
            "si": ["carnivoro", "color_leonado", "rayas_negras"],
            "entonces": ["tigre"],
        },
        {
            "nombre": "R11 - ungulado + cuello_largo + patas_largas → jirafa",
            "si": ["ungulado", "cuello_largo", "patas_largas"],
            "entonces": ["jirafa"],
        },
        {
            "nombre": "R12 - ungulado + rayas_negras → cebra",
            "si": ["ungulado", "rayas_negras"],
            "entonces": ["cebra"],
        },
        {
            "nombre": "R13 - ave + no_vuela + cuello_largo → avestruz",
            "si": ["ave", "no_vuela", "cuello_largo"],
            "entonces": ["avestruz"],
        },
        {
            "nombre": "R14 - ave + no_vuela + nada → pinguino",
            "si": ["ave", "no_vuela", "nada"],
            "entonces": ["pinguino"],
        },
        {
            "nombre": "R15 - ave + buen_volador → albatros",
            "si": ["ave", "buen_volador"],
            "entonces": ["albatros"],
        },
    ]

    bc.cargar_base([], reglas)
    return bc


# ---------------------------------------------------------------------------
# BASE DE CONOCIMIENTO DE EJEMPLO 2 — Clasificación de enfermedades simples
# ---------------------------------------------------------------------------

def construir_base_diagnostico() -> BaseDeConocimiento:
    bc = BaseDeConocimiento()

    reglas = [
        {
            "nombre": "D1 - fiebre + tos → posible_infeccion_respiratoria",
            "si": ["fiebre", "tos"],
            "entonces": ["posible_infeccion_respiratoria"],
        },
        {
            "nombre": "D2 - fiebre + dolor_muscular → posible_gripe",
            "si": ["fiebre", "dolor_muscular"],
            "entonces": ["posible_gripe"],
        },
        {
            "nombre": "D3 - posible_gripe + tos → gripe_confirmada",
            "si": ["posible_gripe", "tos"],
            "entonces": ["gripe_confirmada"],
        },
        {
            "nombre": "D4 - posible_infeccion_respiratoria + dolor_garganta → angina",
            "si": ["posible_infeccion_respiratoria", "dolor_garganta"],
            "entonces": ["angina"],
        },
        {
            "nombre": "D5 - gripe_confirmada → necesita_reposo",
            "si": ["gripe_confirmada"],
            "entonces": ["necesita_reposo"],
        },
        {
            "nombre": "D6 - angina → necesita_antibiotico",
            "si": ["angina"],
            "entonces": ["necesita_antibiotico"],
        },
        {
            "nombre": "D7 - necesita_antibiotico → necesita_medico",
            "si": ["necesita_antibiotico"],
            "entonces": ["necesita_medico"],
        },
        {
            "nombre": "D8 - gripe_confirmada + fiebre_alta → necesita_medico",
            "si": ["gripe_confirmada", "fiebre_alta"],
            "entonces": ["necesita_medico"],
        },
    ]

    bc.cargar_base([], reglas)
    return bc


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

def demo_animales():
    print("\n" + "█" * 60)
    print("  DEMO 1 — Clasificación de Animales")
    print("█" * 60)

    bc = construir_base_animales()

    # Caso 1: tigre
    print("\n--- Caso: animal con pelo, come carne, color leonado, rayas negras ---")
    bc.resetear_hechos(["tiene_pelo", "come_carne", "color_leonado", "rayas_negras"])
    bc.inferir(verbose=True)
    print(f"\n¿Es tigre? → {bc.consultar('tigre')}")
    print(bc.explicar("tigre"))

    # Caso 2: jirafa
    print("\n--- Caso: animal que da leche, tiene pezunas, cuello largo, patas largas ---")
    bc.resetear_hechos(["da_leche", "tiene_pezunas", "cuello_largo", "patas_largas"])
    bc.inferir(verbose=True)
    print(f"\n¿Es jirafa? → {bc.consultar('jirafa')}")
    print(bc.explicar("jirafa"))

    # Caso 3: pingüino
    print("\n--- Caso: animal con plumas, no vuela, nada ---")
    bc.resetear_hechos(["tiene_plumas", "no_vuela", "nada"])
    bc.inferir(verbose=True)
    print(f"\n¿Es pingüino? → {bc.consultar('pinguino')}")
    print(bc.explicar("pinguino"))
    print(f"\n¿Es albatros? → {bc.consultar('albatros')}")


def demo_diagnostico():
    print("\n" + "█" * 60)
    print("  DEMO 2 — Diagnóstico Médico Simple")
    print("█" * 60)

    bc = construir_base_diagnostico()

    # Caso: gripe con fiebre alta
    print("\n--- Síntomas: fiebre, fiebre_alta, tos, dolor_muscular ---")
    bc.resetear_hechos(["fiebre", "fiebre_alta", "tos", "dolor_muscular"])
    bc.inferir(verbose=True)

    print(f"\n¿Gripe confirmada?    → {bc.consultar('gripe_confirmada')}")
    print(f"¿Necesita reposo?     → {bc.consultar('necesita_reposo')}")
    print(f"¿Necesita médico?     → {bc.consultar('necesita_medico')}")
    print(f"¿Necesita antibiótico?→ {bc.consultar('necesita_antibiotico')}")

    print()
    print(bc.explicar("necesita_medico"))

    # Caso: angina
    print("\n--- Síntomas: fiebre, tos, dolor_garganta ---")
    bc.resetear_hechos(["fiebre", "tos", "dolor_garganta"])
    bc.inferir(verbose=True)

    print(f"\n¿Angina?              → {bc.consultar('angina')}")
    print(f"¿Necesita antibiótico?→ {bc.consultar('necesita_antibiotico')}")
    print(f"¿Necesita médico?     → {bc.consultar('necesita_medico')}")
    print()
    print(bc.explicar("angina"))


def demo_interactiva():
    """Modo interactivo: el usuario ingresa hechos y hace consultas."""
    print("\n" + "█" * 60)
    print("  DEMO 3 — Modo Interactivo (Animales)")
    print("█" * 60)

    bc = construir_base_animales()

    print("\nReglas disponibles:")
    for r in bc.listar_reglas():
        print(f"  {r}")

    print("\nIngresá los hechos conocidos del animal (uno por línea).")
    print("Hechos disponibles: tiene_pelo, da_leche, tiene_plumas, vuela,")
    print("  pone_huevos, come_carne, tiene_dientes_afilados, ojos_al_frente,")
    print("  tiene_pezunas, rumia, color_leonado, manchas_oscuras, rayas_negras,")
    print("  cuello_largo, patas_largas, no_vuela, nada, buen_volador")
    print("Escribí 'listo' cuando termines.\n")

    hechos_usuario = []
    while True:
        entrada = input("Hecho: ").strip().lower()
        if entrada == "listo":
            break
        if entrada:
            hechos_usuario.append(entrada)

    if not hechos_usuario:
        print("No ingresaste hechos.")
        return

    bc.resetear_hechos(hechos_usuario)
    todos = bc.inferir(verbose=False)

    print(f"\nTodos los hechos derivados: {sorted(todos)}")

    animales = ["guepardo", "tigre", "jirafa", "cebra", "avestruz", "pinguino", "albatros"]
    print("\nClasificación:")
    for animal in animales:
        if animal in todos:
            print(f"  ✓ Es un {animal.upper()}")
            print(f"    {bc.explicar(animal)}")


# ---------------------------------------------------------------------------
# PUNTO DE ENTRADA
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demo_animales()
    demo_diagnostico()

    print("\n¿Querés probar el modo interactivo? (s/n): ", end="")
    resp = input().strip().lower()
    if resp == "s":
        demo_interactiva()