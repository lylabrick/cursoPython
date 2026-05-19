# main.py
from fastapi import FastAPI
from database import engine
from services.entities.entidades import Base
# Importamos el 'router' de tu controlador
from controller.PersonaController import router as persona_router
from controller.PeliculaController import router as pelicula_router

# AQUÍ es el único lugar donde se crean las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registramos las rutas de personas
# Registramos las rutas de peliculas
app.include_router(persona_router)
app.include_router(pelicula_router)
