# tests/test_cli.py
# pytest tests/

import pytest
import hashlib
from pathlib import Path
from typer.testing import CliRunner
from practica5.cliprofesional import app

runner = CliRunner()


# ──────────────────────────────────────────────
# Tests: hash
# ──────────────────────────────────────────────

def test_hash_sha256_default():
    result = runner.invoke(app, ["hash", "hola mundo"])
    assert result.exit_code == 0
    esperado = hashlib.sha256(b"hola mundo").hexdigest()
    assert esperado in result.output

def test_hash_md5():
    result = runner.invoke(app, ["hash", "hola", "--algo", "md5"])
    assert result.exit_code == 0
    assert hashlib.md5(b"hola").hexdigest() in result.output

def test_hash_algoritmo_invalido():
    result = runner.invoke(app, ["hash", "hola", "--algo", "blake3"])
    assert result.exit_code == 1
    assert "inválido" in result.output.lower() or "inv" in result.output.lower()

def test_hash_archivo(tmp_path):
    archivo = tmp_path / "test.txt"
    archivo.write_text("contenido de prueba")
    result = runner.invoke(app, ["hash", str(archivo), "--file"])
    assert result.exit_code == 0
    esperado = hashlib.sha256(b"contenido de prueba").hexdigest()
    assert esperado in result.output

def test_hash_archivo_inexistente():
    result = runner.invoke(app, ["hash", "/no/existe.txt", "--file"])
    assert result.exit_code == 1


# ──────────────────────────────────────────────
# Tests: buscar
# ──────────────────────────────────────────────

def test_buscar_encuentra_coincidencia(tmp_path):
    (tmp_path / "codigo.py").write_text("def hola():\n    pass\n")
    result = runner.invoke(app, ["buscar", "def hola", "--dir", str(tmp_path), "--ext", "py"])
    assert result.exit_code == 0
    assert "def hola" in result.output

def test_buscar_sin_coincidencias(tmp_path):
    (tmp_path / "archivo.py").write_text("print('mundo')")
    result = runner.invoke(app, ["buscar", "xyz_inexistente", "--dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "0 coincidencia" in result.output

def test_buscar_ignore_case(tmp_path):
    (tmp_path / "archivo.txt").write_text("Hola Mundo")
    result = runner.invoke(app, ["buscar", "hola mundo", "--dir", str(tmp_path), "--ignore-case"])
    assert result.exit_code == 0
    assert "1 coincidencia" in result.output

def test_buscar_directorio_sin_archivos(tmp_path):
    result = runner.invoke(app, ["buscar", "algo", "--dir", str(tmp_path), "--ext", "py"])
    assert result.exit_code == 0
    assert "No se encontraron" in result.output


# ──────────────────────────────────────────────
# Tests: info-proyecto
# ──────────────────────────────────────────────

def test_info_proyecto_tabla(tmp_path):
    (tmp_path / "main.py").write_text("print('hola')\nprint('mundo')\n")
    result = runner.invoke(app, ["info-proyecto", "--dir", str(tmp_path), "--ext", "py"])
    assert result.exit_code == 0
    assert "py" in result.output
    assert "2" in result.output  # 2 líneas

def test_info_proyecto_json(tmp_path):
    (tmp_path / "app.py").write_text("x = 1\n")
    result = runner.invoke(app, ["info-proyecto", "--dir", str(tmp_path), "--ext", "py", "--formato", "json"])
    assert result.exit_code == 0
    import json
    data = json.loads(result.output)
    assert "py" in data
    assert data["py"]["archivos"] == 1

def test_info_proyecto_sin_archivos(tmp_path):
    result = runner.invoke(app, ["info-proyecto", "--dir", str(tmp_path), "--ext", "xyz"])
    assert result.exit_code == 0
    assert "No se encontraron" in result.output