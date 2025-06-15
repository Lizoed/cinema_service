from typing import List
from datetime import datetime
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Screening(Base):
    __tablename__ = "screening"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    price: Mapped[float]
    status: Mapped[bool] = mapped_column(default=True)

    film_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("film.id")
    )
    cinema_hall_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cinema_hall.id")
    )

    film: Mapped["Film"] = relationship("Film", back_populates="screenings")
    cinema_hall: Mapped["CinemaHall"] = relationship("CinemaHall", back_populates="screenings")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="screening")