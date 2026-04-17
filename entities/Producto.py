from dataclasses import dataclass, field

@dataclass
class Producto:
    id: int
    nombre: str
    precio: float
    stock: int 

    def __post_init__(self):
        if self.id <= 0:
            raise ValueError(f"El id debe ser mayor a 0, se recibio {self.id}")
        
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre no puede ser vacio")
        
        if self.precio < 0:
            raise ValueError(f"El precio no puede ser negativo, se recibio {self.precio}")  
        
        if self.stock < 0:
            raise ValueError(f"El stock no puede ser negativo, se recibio {self.stock}")    
        
        