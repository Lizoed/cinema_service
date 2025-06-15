from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from app.models import booking as models
from app.models import screening as screening_models
from app.schemas.booking import BookingCreate


def create_booking(db: Session, booking: BookingCreate):
    screening = db.query(screening_models.Screening).filter(screening_models.Screening.id == booking.screening_id).first()

    if not screening or screening.start_time <= datetime.now():
        return None

    existing_booking = db.query(models.Booking).filter(
        models.Booking.screening_id == booking.screening_id,
        models.Booking.seat_id == booking.seat_id).first()

    if existing_booking:
        return None

    db_booking = models.Booking(
        screening_id=booking.screening_id,
        seat_id=booking.seat_id,
        client_name=booking.client_name
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def cancel_booking(db: Session, booking_id: UUID):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()

    if not booking:
        return False

    screening = db.query(screening_models.Screening).filter(screening_models.Screening.id == booking.screening_id).first()

    if screening and screening.start_time <= datetime.now():
        return False

    db.delete(booking)
    db.commit()
    return True