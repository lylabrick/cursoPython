from typing import Optional
from biblioteca.Socio import Socio
from biblioteca.persistencia.RepositorioSocios import RepositorioSocios

class RepositorioSociosMemoria(RepositorioSocios):

    def __init__(self):
        self._socios: dict[int, "Socio"] = {}
    
    def guardar(self, socio: "Socio"):
        self._socios[socio.numero_socio] = socio

    def buscar_por_numero(self, numero_socio: int) -> Optional["Socio"]:
        return self._socios.get(numero_socio)

    def listar_todos(self) -> list["Socio"]:
        return list(self._socios.values())  