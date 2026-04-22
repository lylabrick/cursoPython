from biblioteca.Autor import Autor
from biblioteca.Libro import Libro
from biblioteca.Socio import Socio
from biblioteca.Biblioteca import Biblioteca
from biblioteca.Prestamo import Prestamo
from datetime import date
from biblioteca.MultaPorDia import MultaPorDia
from biblioteca.MultaPorCategoria import MultaPorCategoria
from biblioteca.MultaTarifaFija import MultaTarifaFija
from biblioteca.MultaEscalonada import MultaEscalonada

autor = Autor("Borges", "borges@email.com", "Argentina")
socio = Socio("Laura", "laura@email.com", 1)

libro1 = Libro("Ficciones",      autor, "978-123", "novela")
libro2 = Libro("Física Cuántica", autor, "978-456", "ciencia")
libro3 = Libro("El Principito",   autor, "978-789", "infantil")

fecha_prestamo = date(2024, 1, 1)
fecha_limite   = date(2024, 1, 8)
fecha_tardía   = date(2024, 1, 18)   # 10 días de retraso

# ── Estrategia 1: por día
biblioteca = Biblioteca("Biblioteca Central", MultaPorDia(tarifa_por_dia=100))
biblioteca.agregar_libro(libro1)
biblioteca.registrar_socio(socio)

prestamo = Prestamo(libro1, socio, fecha_limite, MultaPorDia(100), fecha_prestamo)
prestamo.devolver(fecha_tardía)
print(f"Multa por día:      ${prestamo.calcular_multa():.2f}")   # → $1000.00

# ── Estrategia 2: por categoría
prestamo2 = Prestamo(libro2, socio, fecha_limite, MultaPorCategoria(), fecha_prestamo)
prestamo2.devolver(fecha_tardía)
print(f"Multa por categoría: ${prestamo2.calcular_multa():.2f}") # → $1500.00 (ciencia)

prestamo3 = Prestamo(libro3, socio, fecha_prestamo, MultaPorCategoria(), fecha_prestamo)
prestamo3.devolver(fecha_tardía)
print(f"Multa infantil:      ${prestamo3.calcular_multa():.2f}") # → $500.00

# ── Estrategia 3: tarifa fija
prestamo4 = Prestamo(libro1, socio, fecha_limite, MultaTarifaFija(500), fecha_prestamo)
prestamo4.devolver(fecha_tardía)
print(f"Multa fija:          ${prestamo4.calcular_multa():.2f}") # → $500.00

# ── Estrategia 4: escalonada
prestamo5 = Prestamo(libro1, socio, fecha_limite, MultaEscalonada(),  fecha_prestamo)
prestamo5.devolver(fecha_tardía)
print(f"Multa escalonada:    ${prestamo5.calcular_multa():.2f}") # → $1000.00 (10 días × $100)

# ── Cambio de estrategia en tiempo de ejecución
prestamo5.cambiar_estrategia(MultaTarifaFija(200))
print(f"Tras cambio:         ${prestamo5.calcular_multa():.2f}") # → $200.00
