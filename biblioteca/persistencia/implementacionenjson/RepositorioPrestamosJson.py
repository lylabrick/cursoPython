from biblioteca.persistencia.RepositorioPrestamos import RepositorioPrestamos
from biblioteca.Prestamo import Prestamo
import json
import os
from typing import Optional

class RepositorioPrestamosJson(RepositorioPrestamos):
    def __init__(self, ruta: str = "prestamos.json"):
        self._ruta = ruta
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        if not os.path.exists(self._ruta):
            self._escribir([])

    def _leer(self) -> list:
        with open(self._ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _escribir(self, datos: list):
        with open(self._ruta,"w", encoding="utf=8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    
    def _serializar(self, prestamo:"Prestamo") -> dict:
        return{
            "isbn": prestamo.libro.isbn,
            "numero_socio": prestamo.socio.numero_socio,
            "fecha_inicio": str(prestamo._fecha_inicio),
            "fecha_limite": str(prestamo._fecha_limite),
            "fecha_devolucion": str(prestamo._fecha_devolucion) if prestamo._fecha_devolucion else None,
        }
    
    def guardar(self, prestamo: "Prestamo"):
        datos = self._leer()
        datos.append(self._serializar(prestamo))
        self._escribir(datos)

    def listar_archivos(self) -> list["Prestamo"]:
        datos = self._leer()
        return[d for d in datos if d["fecha_devolucion"] is None]

    def buscar_archivo_por_isbn(self, isbn: str) -> Optional["Prestamo"]:
        datos = self._leer()
        for d in datos: 
            if d["isbn"] == isbn and d["fecha_devolucion"] is None:
                 return d
        return None