from sqlalchemy.orm import Session
from uuid import UUID
from  app.models.cinema_hall import CinemaHall
from app.models.seat import Seat
from app.schemas.cinema_hall import CinemaHallCreate

def create_cinema_hall(db: Session, cinema_hall: CinemaHallCreate):
    db_cinema_hall = CinemaHall(
        address=cinema_hall.address,
        capacity=cinema_hall.capacity,
        opening_time=cinema_hall.opening_time,
        closing_time=cinema_hall.closing_time
    )
    db.add(db_cinema_hall)
    db.commit()
    db.refresh(db_cinema_hall)

    for i in range(1, cinema_hall.capacity + 1):
        db_seat = Seat(
            number=i,
            cinema_hall_id=db_cinema_hall.id
        )
        db.add(db_seat)
    db.commit()

    db.refresh(db_cinema_hall)
    return db_cinema_hall

def get_cinema_halls(db: Session):
    return db.query(CinemaHall).all()

def get_cinema_hall(db: Session, cinema_hall_id: UUID):
    return db.query(CinemaHall).filter(CinemaHall.id == cinema_hall_id).first()