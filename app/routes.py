from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.service import (
    cinema_hall as cinema_hall_service,
    film as film_service,
    screening as screening_service,
    booking as booking_service
)
from app.schemas import (
    cinema_hall as cinema_hall_schem,
    film as film_schem,
    screening as screening_schem,
    booking as booking_schem
)
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed")
    finally:
        db.close()

@router.post("/cinema_hall/", response_model=cinema_hall_schem.CinemaHall)
def create_cinema_hall(cinema_hall: cinema_hall_schem.CinemaHallCreate):
    try:
        return cinema_hall_service.create_cinema_hall(db=SessionLocal(), cinema_hall=cinema_hall)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating cinema hall: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not create cinema hall")

@router.get("/cinema_hall/", response_model=list[cinema_hall_schem.CinemaHallBase])
def get_cinema_halls():
    try:
        halls = cinema_hall_service.get_cinema_halls(db=SessionLocal())
        if not halls:
            raise HTTPException(status_code=404, detail="No cinema halls found")
        return halls
    except Exception as e:
        logger.error(f"Error fetching cinema halls: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve cinema halls")

@router.get("/cinema_hall/{cinema_hall_id}", response_model=cinema_hall_schem.CinemaHallDetailed)
def get_cinema_hall(cinema_hall_id: UUID):
    db = SessionLocal()
    try:
        cinema_hall = cinema_hall_service.get_cinema_hall(db, cinema_hall_id)
        if not cinema_hall:
            raise HTTPException(status_code=404, detail="Cinema hall not found")
        return cinema_hall
    except Exception as e:
        logger.error(f"Error fetching cinema hall {cinema_hall_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve cinema hall information")

@router.post("/film/", response_model=film_schem.Film)
def create_film(film: film_schem.FilmCreate):
    try:
        return film_service.create_film(db=SessionLocal(), film=film)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating film: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not create film")

@router.get("/film/", response_model=list[film_schem.FilmWithStatus])
def get_films(is_active: bool = None):
    try:
        films = film_service.get_films(db=SessionLocal(), is_active=is_active)
        if not films:
            raise HTTPException(status_code=404, detail="No films found matching criteria")
        return films
    except Exception as e:
        logger.error(f"Error fetching films: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve films")

@router.post("/screening/", response_model=screening_schem.Screening)
def create_screening(screening: screening_schem.ScreeningCreate):
    db = SessionLocal()
    try:
        result = screening_service.create_screening(db=db, screening=screening)
        if not result:
            raise HTTPException(status_code=400, detail="Time conflict with another screening or outside working hours")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating screening: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not create screening")

@router.get("/screening/", response_model=list[screening_schem.ScreeningBase])
def get_screenings(cinema_hall_id: UUID = None, film_id: UUID = None):
    try:
        screenings = screening_service.get_screenings(
            db=SessionLocal(),
            cinema_hall_id=cinema_hall_id,
            film_id=film_id
        )
        if not screenings:
            raise HTTPException(status_code=404, detail="No screenings found matching criteria")
        return screenings
    except Exception as e:
        logger.error(f"Error fetching screenings: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve screenings")

@router.get("/screening/{screening_id}", response_model=screening_schem.ScreeningDetailed)
def get_screening(screening_id: UUID):
    db = SessionLocal()
    try:
        screening = screening_service.get_screening_detailed(db, screening_id)
        if not screening:
            raise HTTPException(status_code=404, detail="Screening not found")
        return screening
    except Exception as e:
        logger.error(f"Error fetching screening {screening_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve screening information")

@router.post("/booking/", response_model=booking_schem.Booking)
def create_booking(booking: booking_schem.BookingCreate):
    db = SessionLocal()
    try:
        result = booking_service.create_booking(db=db, booking=booking)
        if not result:
            raise HTTPException(status_code=400, detail="Seat already booked or screening started")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not create booking")

@router.delete("/booking/{booking_id}")
def cancel_booking(booking_id: UUID):
    db = SessionLocal()
    try:
        success = booking_service.cancel_booking(db=db, booking_id=booking_id)
        if not success:
            raise HTTPException(status_code=400, detail="Cannot cancel booking after screening started")
        return {"message": "Booking cancelled successfully"}
    except Exception as e:
        logger.error(f"Error cancelling booking {booking_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not cancel booking")