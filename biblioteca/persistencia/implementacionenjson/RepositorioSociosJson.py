from biblioteca.persistencia.RepositorioSocios import RepositorioSocios
import json
import os
from typing import Optional
from biblioteca.Socio import Socio

class RepositorioSociosJson(RepositorioSocios):
    def __init__(self, ruta: str = "socios.json"):
        self._ruta = ruta
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        if not os.path.exists(self._ruta):
            self._escribir({})

    def _leer(self) -> dict:
        with open(self._ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def _escribir(self, datos: dict):
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    
    def _serializar(self, socio: "Socio") -> dict:
        return {
            "nombre": socio.nombre,
            "email": socio.email,
            "numero_socio": socio.numero_socio,
        }
    
    def _deserializar(self, datos: dict) -> "Socio":
        return Socio(
            datos["nombre"],
            datos["email"],
            datos["numero_socio"],
        )
        
    def guardar(self, socio: "Socio"):
        datos = self._leer()
        datos[str(socio.numero_socio)] = self._serializar(socio)
        self._escribir(datos)
        
    def buscar_por_numero(self, numero_socio: int) -> Optional["Socio"]:
        datos = self._leer()
        if str(numero_socio) in datos:
            return self._deserializar(datos[str(numero_socio)])
        return None
    
    def listar_todos(self) -> list["Socio"]:
        datos = self._leer()
        return [self._deserializar(d) for d in datos.values()]
        
            
