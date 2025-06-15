from datetime import datetime
from typing import List
from pydantic import BaseModel
from uuid import UUID
from app.schemas.base import BaseSchema
from app.schemas.cinema_hall import CinemaHallBase, SeatBase
from app.schemas.film import FilmBase

class ScreeningBase(BaseSchema):
    id: UUID
    start_time: datetime
    price: float

class ScreeningCreate(BaseModel):
    start_time: datetime
    price: float
    film_id: UUID
    cinema_hall_id: UUID

class Screening(ScreeningBase):
    end_time: datetime
    film: FilmBase
    cinema_hall: CinemaHallBase

class ScreeningDetailed(ScreeningBase):
    end_time: datetime
    film: FilmBase
    cinema_hall: CinemaHallBase
    free_seats: List[SeatBase]