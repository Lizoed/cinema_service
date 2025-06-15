from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import UUID
from app.models.screening import Screening
from app.models.cinema_hall import CinemaHall
from app.models.film import Film
from app.models.seat import Seat
from app.models.booking import Booking
from app.schemas.screening import ScreeningCreate


def create_screening(db: Session, screening: ScreeningCreate):
    cinema_hall = db.query(CinemaHall).filter(CinemaHall.id == screening.cinema_hall_id).first()

    film = db.query(Film).filter(Film.id == screening.film_id).first()

    if not cinema_hall or not film:
        return None

    end_time = screening.start_time + timedelta(minutes=film.duration)

    if (screening.start_time.time() < cinema_hall.opening_time or
            end_time.time() > cinema_hall.closing_time):
        return None

    overlapping = db.query(Screening).filter(
        Screening.cinema_hall_id == screening.cinema_hall_id,
        Screening.start_time < end_time,
        Screening.end_time > screening.start_time).first()

    if overlapping:
        return None

    db_screening = Screening(
        start_time=screening.start_time,
        end_time=end_time,
        price=screening.price,
        film_id=screening.film_id,
        cinema_hall_id=screening.cinema_hall_id
    )
    db.add(db_screening)
    db.commit()
    db.refresh(db_screening)
    return db_screening


def get_screenings(db: Session, cinema_hall_id: UUID = None, film_id: UUID = None):
    query = db.query(Screening)

    if cinema_hall_id:
        query = query.filter(Screening.cinema_hall_id == cinema_hall_id)
    if film_id:
        query = query.filter(Screening.film_id == film_id)

    return query.all()


def get_screening_detailed(db: Session, screening_id: UUID):
    screening = db.query(Screening).filter(Screening.id == screening_id).first()

    if not screening:
        return None

    seats = db.query(Seat).filter(Seat.cinema_hall_id == screening.cinema_hall_id).all()

    booked_seats = db.query(Booking).filter(Booking.screening_id == screening_id).all()

    booked_seat_ids = {booking.seat_id for booking in booked_seats}
    free_seats = [seat for seat in seats if seat.id not in booked_seat_ids]

    return {
        "id": screening.id,
        "start_time": screening.start_time,
        "end_time": screening.end_time,
        "price": screening.price,
        "film": {
            "id": screening.film.id,
            "name": screening.film.name,
            "duration": screening.film.duration
        },
        "cinema_hall": {
            "id": screening.cinema_hall.id,
            "address": screening.cinema_hall.address,
            "capacity": screening.cinema_hall.capacity
        },
        "free_seats": [{"id": seat.id, "number": seat.number} for seat in free_seats]
    }