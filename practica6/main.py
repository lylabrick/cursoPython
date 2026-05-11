# main.py
from fastapi import FastAPI
from database import engine
from services.entities.entidades import Base
# Importamos el 'router' de tu controlador
from controller.PersonaController import router as persona_router

# AQUÍ es el único lugar donde se crean las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registramos las rutas de personas
app.include_router(persona_router)

# Si luego tienes PeliculaController, solo lo agregas aquí:
# from controller.PeliculaController import router as pelicula_router
# app.include_router(pelicula_router)
