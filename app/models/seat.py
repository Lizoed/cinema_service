from typing import List
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Seat(Base):
    __tablename__ = "seat"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    number: Mapped[int]
    cinema_hall_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cinema_hall.id")
    )

    cinema_hall: Mapped["CinemaHall"] = relationship("CinemaHall", back_populates="seats")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="seat")