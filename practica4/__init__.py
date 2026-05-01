from kanren import Relation, facts, run, var, conde, eq

padre = Relation()
madre = Relation()

facts(padre,
    ("juan", "carlos"),
    ("juan", "ana"),
    ("pedro", "juan"),
    ("pedro", "lucia"),
    ("carlos", "mario"),
    ("carlos", "sofia"),
)

facts(madre,
    ("maria", "carlos"),
    ("maria", "ana"),
    ("lucia", "pedro"),
    ("sofia", "rosa"),
)

def padre_o_madre(p, h):
    return conde(
        [padre(p, h)],
        [madre(p, h)]
    )

def abuelo(ab, ni):
    x = var()
    return conde(
        [padre(ab, x), padre_o_madre(x, ni)],
        [madre(ab, x), padre_o_madre(x, ni)]
    )

def hermano(h1, h2):
    p = var()
    return conde(
        [padre(p, h1), padre(p, h2)]
    )

def primo(p1, p2):
    padre1 = var()
    padre2 = var()
    return conde(
        [padre_o_madre(padre1, p1),
         padre_o_madre(padre2, p2),
         hermano(padre1, padre2)]
    )

x = var()

print("=== Hijos de juan ===")
print(run(0, x, padre("juan", x)))

print("\n=== Padres de carlos ===")
print(run(0, x, padre_o_madre(x, "carlos")))

print("\n=== Abuelos de mario ===")
print(run(0, x, abuelo(x, "mario")))

print("\n=== Nietos de pedro ===")
print(run(0, x, abuelo("pedro", x)))

print("\n=== Hermanos de carlos ===")
y = var()
print([r for r in run(0, x, hermano(x, "carlos")) if x != "carlos"])

print("\n=== Primos de mario ===")
print([r for r in run(0, x, primo(x, "mario")) if r != "mario"])

print("\n=== Todos los pares abuelo-nieto ===")
ab, ni = var(), var()
resultados = run(0, (ab, ni), abuelo(ab, ni))
for par in set(resultados):
    print(f"  {par[0]} es abuelo/a de {par[1]}")