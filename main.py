from utils import flatten_ejercicio1
from entities import Producto

print(flatten_ejercicio1([1, [2, [3, [4]], 5]]))
print(flatten_ejercicio1(["primero", ["segundo", ["tercero", ["cuarto"]], "quinto"]]))
print(flatten_ejercicio1([1, [2, [3, [4]], 5]]))

p = Producto(id=1, nombre="Teclado", precio=5999.99, stock=10)
print(p)