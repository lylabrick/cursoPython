from utils import flatten_ejercicio1
from entities import Producto
from colorama import Fore, Style
from biblioteca.Autor import Autor
from biblioteca.Libro import Libro
from biblioteca.Socio import Socio
from biblioteca.Biblioteca import Biblioteca

print(Fore.GREEN + str(flatten_ejercicio1([1, [2, [3, [4]], 5]])))
print(Fore.BLUE + str(flatten_ejercicio1(["primero", ["segundo", ["tercero", ["cuarto"]], "quinto"]])))
print(Fore.RED + str(flatten_ejercicio1([1, [2, [3, [4]], 5]])))

p = Producto(id=1, nombre="Teclado", precio=5999.99, stock=10)
print(p)

autor = Autor("Borges", "borges@email.com", "Argentina")
socio = Socio("Laura", "laura@email.com", 1)
libro = Libro("Ficciones", autor, "978-123")

biblioteca = Biblioteca("Biblioteca Central")
biblioteca.agregar_libro(libro)
biblioteca.registrar_socio(socio)

prestamo = biblioteca.prestar_libro("978-123", socio)
print(Fore.CYAN + str(prestamo))
# → Préstamo de Ficciones a Laura [activo]

print("libros disponibles" + str(biblioteca.libros_disponibles()))
# → []

biblioteca.devolver_libro("978-123")
print(prestamo)
# → Préstamo de Ficciones a Laura [devuelto el 2024-01-15]