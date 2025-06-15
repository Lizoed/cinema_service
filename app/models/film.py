from typing import List
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Film(Base):
    __tablename__ = "film"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str]
    duration: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)

    screenings: Mapped[List["Screening"]] = relationship("Screening", back_populates="film")