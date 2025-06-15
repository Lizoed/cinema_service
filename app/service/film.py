from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from app.models.film import Film
from app.models.screening import Screening
from app.schemas.film import FilmCreate


def create_film(db: Session, film: FilmCreate):
    db_film = Film(
        name=film.name,
        duration=film.duration
    )
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film


def get_films(db: Session, is_active: bool = None):
    films = db.query(Film).all()
    result = []

    for film in films:
        screenings = db.query(Screening).filter(Screening.film_id == film.id).all()

        active = any(
            screening.start_time > datetime.now()
            for screening in screenings
        )

        if is_active is None or active == is_active:
            result.append({
                "id": film.id,
                "name": film.name,
                "duration": film.duration,
                "is_active": active
            })

    return result