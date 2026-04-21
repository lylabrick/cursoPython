from utils import flatten_ejercicio1
from entities import Producto
from colorama import Fore, Style
from biblioteca.Autor import Autor
from biblioteca.Libro import Libro
from biblioteca.Socio import Socio
from biblioteca.Biblioteca import Biblioteca

"""
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
 """


autor = Autor("Borges", "borges@email.com", "Argentina")
biblioteca = Biblioteca("Biblioteca Central")

libro = Libro("Ficciones", autor, "978-123")
socio1 = Socio("Laura", "laura@email.com", 1)
socio2 = Socio("Ana",   "ana@email.com",   2)
socio3 = Socio("Juan",  "juan@email.com",  3)

biblioteca.agregar_libro(libro)
biblioteca.registrar_socio(socio1)
biblioteca.registrar_socio(socio2)
biblioteca.registrar_socio(socio3)

# socio1 pide el libro
prestamo = biblioteca.prestar_libro("978-123", socio1)
print(prestamo)
# → Préstamo de 'Ficciones' a Laura [activo]

# socio2 y socio3 se anotan en lista de espera
biblioteca.agregar_a_lista_de_espera("978-123", socio2)
biblioteca.agregar_a_lista_de_espera("978-123", socio3)

print(libro)
# → 'Ficciones' de Borges [prestado] — 2 en lista de espera

# socio1 devuelve → notifica a socio2 y socio3
biblioteca.devolver_libro("978-123")
# → 📬 [Ana] El libro 'Ficciones' ya está disponible
# → 📬 [Juan] El libro 'Ficciones' ya está disponible

print(prestamo)
# → Préstamo de 'Ficciones' a Laura [devuelto el 2024-01-15]

print(biblioteca.prestamos_activos())