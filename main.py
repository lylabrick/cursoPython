from utils import flatten_ejercicio1
from entities import Producto
from colorama import Fore, Style

print(Fore.GREEN + str(flatten_ejercicio1([1, [2, [3, [4]], 5]])))
print(Fore.BLUE + str(flatten_ejercicio1(["primero", ["segundo", ["tercero", ["cuarto"]], "quinto"]])))
print(Fore.RED + str(flatten_ejercicio1([1, [2, [3, [4]], 5]])))

p = Producto(id=1, nombre="Teclado", precio=5999.99, stock=10)
print(p)