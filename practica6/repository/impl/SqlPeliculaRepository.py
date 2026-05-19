from services.entities.entidades import Pelicula
from repository.PeliculaRepository import PeliculaRepository
from typing import Optional

class SQLPeliculaRepository(PeliculaRepository):
    def __init__(self, db_session):
        self.session = db_session

    def save(self, pelicula: Pelicula) -> Pelicula:
        self.session.add(pelicula)
        self.session.commit()
        return pelicula

    def find_by_id(self, pelicula_id: int) -> Optional[Pelicula]:
        result = self.session.query(Pelicula).filter_by(id=pelicula_id).first()
        if not result:
            return None
        return result

    def find_all(self):
        return self.session.query(Pelicula).all()

    def delete(self, pelicula_id: int) -> bool:
        pelicula = self.find_by_id(pelicula_id)
        if pelicula:
            self.session.delete(pelicula)
            self.session.commit()
            return True
        return False

    def find_by_genero(self, genero: str) -> list[Pelicula]:
        return self.session.query(Pelicula).filter_by(genero=genero).all()