# practica6/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.entities.entidades import Base

engine = create_engine("postgresql://postgres:tu_password@localhost:5432/postgres", echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
