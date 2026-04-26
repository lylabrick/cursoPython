# tests/test_repos_json.py
from datetime import date
from unittest.mock import MagicMock, mock_open, patch

import pytest

from biblioteca.Autor import Autor
from biblioteca.Libro import Libro
from biblioteca.Prestamo import Prestamo
from biblioteca.Socio import Socio
from biblioteca.persistencia.implementacionenjson.RepositorioLibrosJson import (
    RepositorioLibrosJson,
)
from biblioteca.persistencia.implementacionenjson.RepositorioPrestamosJson import (
    RepositorioPrestamosJson,
)
from biblioteca.persistencia.implementacionenjson.RepositorioSociosJson import (
    RepositorioSociosJson,
)


def test_repo_libros_json_asegura_archivo_si_no_existe():
    with patch("biblioteca.persistencia.implementacionenjson.RepositorioLibrosJson.os.path.exists", return_value=False):
        with patch.object(RepositorioLibrosJson, "_escribir") as escribir:
            RepositorioLibrosJson("libros.json")
            escribir.assert_called_once_with({})


def test_repo_socios_json_asegura_archivo_si_no_existe():
    with patch("biblioteca.persistencia.implementacionenjson.RepositorioSociosJson.os.path.exists", return_value=False):
        with patch.object(RepositorioSociosJson, "_escribir") as escribir:
            RepositorioSociosJson("socios.json")
            escribir.assert_called_once_with({})


def test_repo_prestamos_json_asegura_archivo_si_no_existe():
    with patch("biblioteca.persistencia.implementacionenjson.RepositorioPrestamosJson.os.path.exists", return_value=False):
        with patch.object(RepositorioPrestamosJson, "_escribir") as escribir:
            RepositorioPrestamosJson("prestamos.json")
            escribir.assert_called_once_with([])


def test_repo_libros_json_serializa_y_deserializa():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")

    with patch("biblioteca.persistencia.implementacionenjson.RepositorioLibrosJson.os.path.exists", return_value=True):
        repo = RepositorioLibrosJson("libros.json")

    datos = repo._serializar(libro)
    libro2 = repo._deserializar(datos)

    assert libro2.titulo == "Ficciones"
    assert libro2.isbn == "978-123"
    assert libro2.categoria == "novela"
    assert libro2.autor.nombre == "Borges"
    assert libro2.autor.nacionalidad == "Argentina"


def test_repo_socios_json_guardar_buscar_listar_sin_io_real():
    socio = Socio("Laura", "laura@email.com", 1)

    with patch("biblioteca.persistencia.implementacionenjson.RepositorioSociosJson.os.path.exists", return_value=True):
        repo = RepositorioSociosJson("socios.json")

    repo._leer = MagicMock(return_value={})
    repo._escribir = MagicMock()

    repo.guardar(socio)
    repo._escribir.assert_called_once()
    escrito = repo._escribir.call_args[0][0]
    assert "1" in escrito
    assert escrito["1"]["nombre"] == "Laura"

    repo._leer = MagicMock(return_value=escrito)
    assert repo.buscar_por_numero(1).numero_socio == 1
    assert len(repo.listar_todos()) == 1


def test_repo_prestamos_json_guardar_y_listar_archivos_devuelve_dicts():
    autor = Autor("Borges", "borges@email.com", "Argentina")
    libro = Libro("Ficciones", autor, "978-123", "novela")
    socio = Socio("Laura", "laura@email.com", 1)
    libro.prestar()

    prestamo = Prestamo(libro, socio, date(2026, 4, 25), date(2026, 5, 2))

    with patch("biblioteca.persistencia.implementacionenjson.RepositorioPrestamosJson.os.path.exists", return_value=True):
        repo = RepositorioPrestamosJson("prestamos.json")

    repo._leer = MagicMock(return_value=[])
    repo._escribir = MagicMock()

    repo.guardar(prestamo)
    repo._escribir.assert_called_once()
    guardado = repo._escribir.call_args[0][0]
    assert isinstance(guardado, list)
    assert guardado[0]["isbn"] == "978-123"
    assert guardado[0]["fecha_devolucion"] is None

    repo._leer = MagicMock(return_value=guardado)
    activos = repo.listar_archivos()
    assert len(activos) == 1
    assert activos[0]["isbn"] == "978-123"

    encontrado = repo.buscar_archivo_por_isbn("978-123")
    assert encontrado["numero_socio"] == 1