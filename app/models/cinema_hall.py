from typing import List
from datetime import time
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class CinemaHall(Base):
    __tablename__ = "cinema_hall"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    address: Mapped[str]
    capacity: Mapped[int]
    opening_time: Mapped[time]
    closing_time: Mapped[time]

    seats: Mapped[List["Seat"]] = relationship("Seat", back_populates="cinema_hall")
    screenings: Mapped[List["Screening"]] = relationship("Screening", back_populates="cinema_hall")