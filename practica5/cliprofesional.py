# cli_devtools.py
# pip install typer rich pytest

import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re

app = typer.Typer(help="DevTools CLI — utilidades para desarrolladores.")
console = Console()


# ──────────────────────────────────────────────
# Comando 1: hash
# ──────────────────────────────────────────────

@app.command()
def hash(
    texto: str = typer.Argument(..., help="Texto o ruta de archivo a hashear."),
    algoritmo: str = typer.Option("sha256", "--algo", "-a", help="Algoritmo: md5, sha1, sha256, sha512."),
    es_archivo: bool = typer.Option(False, "--file", "-f", help="Tratar el argumento como ruta de archivo."),
):
    """Calcula el hash de un texto o archivo."""
    algoritmos = {"md5", "sha1", "sha256", "sha512"}
    if algoritmo not in algoritmos:
        rprint(f"[red]Algoritmo inválido. Opciones: {', '.join(algoritmos)}[/red]")
        raise typer.Exit(code=1)

    if es_archivo:
        path = Path(texto)
        if not path.exists():
            rprint(f"[red]Archivo no encontrado: {texto}[/red]")
            raise typer.Exit(code=1)
        contenido = path.read_bytes()
    else:
        contenido = texto.encode()

    resultado = hashlib.new(algoritmo, contenido).hexdigest()
    rprint(f"[bold cyan]{algoritmo.upper()}:[/bold cyan] {resultado}")


# ──────────────────────────────────────────────
# Comando 2: buscar
# ──────────────────────────────────────────────

@app.command()
def buscar(
    patron: str = typer.Argument(..., help="Expresión regular a buscar."),
    directorio: Path = typer.Option(".", "--dir", "-d", help="Directorio donde buscar."),
    extension: str = typer.Option("*", "--ext", "-e", help="Extensión de archivos, ej: py, txt."),
    ignorar_mayusculas: bool = typer.Option(False, "--ignore-case", "-i", help="Búsqueda sin distinción de mayúsculas."),
):
    """Busca un patrón regex en archivos de un directorio."""
    flags = re.IGNORECASE if ignorar_mayusculas else 0
    glob = f"**/*.{extension}" if extension != "*" else "**/*"
    archivos = [f for f in Path(directorio).glob(glob) if f.is_file()]

    if not archivos:
        rprint("[yellow]No se encontraron archivos.[/yellow]")
        raise typer.Exit()

    tabla = Table(title=f"Resultados para: [bold]{patron}[/bold]")
    tabla.add_column("Archivo", style="cyan")
    tabla.add_column("Línea", justify="right", style="yellow")
    tabla.add_column("Contenido", style="white")

    total = 0
    for archivo in archivos:
        try:
            for num, linea in enumerate(archivo.read_text(errors="ignore").splitlines(), 1):
                if re.search(patron, linea, flags):
                    tabla.add_row(str(archivo), str(num), linea.strip()[:80])
                    total += 1
        except Exception:
            continue

    console.print(tabla)
    rprint(f"\n[bold green]{total} coincidencia(s) encontrada(s).[/bold green]")


# ──────────────────────────────────────────────
# Comando 3: info-proyecto
# ──────────────────────────────────────────────

@app.command()
def info_proyecto(
    directorio: Path = typer.Option(".", "--dir", "-d", help="Directorio raíz del proyecto."),
    formato: str = typer.Option("tabla", "--formato", "-f", help="Formato de salida: tabla o json."),
    extensiones: str = typer.Option("py,js,ts,java,swift", "--ext", "-e", help="Extensiones a contar, separadas por coma."),
):
    """Muestra estadísticas de un proyecto: archivos, líneas de código y tamaño."""
    exts = [e.strip() for e in extensiones.split(",")]
    stats = {}

    for ext in exts:
        archivos = list(Path(directorio).rglob(f"*.{ext}"))
        lineas = 0
        bytes_total = 0
        for f in archivos:
            try:
                lineas += len(f.read_text(errors="ignore").splitlines())
                bytes_total += f.stat().st_size
            except Exception:
                continue
        if archivos:
            stats[ext] = {
                "archivos": len(archivos),
                "lineas": lineas,
                "tamanio_kb": round(bytes_total / 1024, 2),
            }

    if not stats:
        rprint("[yellow]No se encontraron archivos con esas extensiones.[/yellow]")
        raise typer.Exit()

    if formato == "json":
        rprint(json.dumps(stats, indent=2))
    else:
        tabla = Table(title=f"Estadísticas: [bold]{Path(directorio).resolve().name}[/bold]")
        tabla.add_column("Extensión", style="cyan")
        tabla.add_column("Archivos", justify="right")
        tabla.add_column("Líneas", justify="right", style="green")
        tabla.add_column("Tamaño (KB)", justify="right", style="yellow")
        for ext, data in stats.items():
            tabla.add_row(f".{ext}", str(data["archivos"]), str(data["lineas"]), str(data["tamanio_kb"]))
        console.print(tabla)


if __name__ == "__main__":
    app()