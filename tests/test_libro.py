from biblioteca.Autor import Autor
from biblioteca.Libro import Libro


def test_propiedades_basicas():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")

    assert libro.titulo == "Ficciones"
    assert libro.autor is autor
    assert libro.isbn == "978-123"
    assert libro.categoria == "novela"
    assert libro.disponible is True


def test_categoria_default_y_disponible_default():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123")  # categoria default

    assert libro.categoria == "novela"
    assert libro.disponible is True


def test_prestar_y_devolver_cambian_disponible():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")

    libro.prestar()
    assert libro.disponible is False

    libro.devolver()
    assert libro.disponible is True


def test_str_formato():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")

    assert str(libro) == "'Ficciones' [novela]"