from datetime import time
from typing import List
from pydantic import BaseModel
from uuid import UUID
from app.schemas.base import BaseSchema

class SeatBase(BaseSchema):
    id: UUID
    number: int

class CinemaHallBase(BaseSchema):
    id: UUID
    address: str
    capacity: int

class CinemaHallCreate(BaseModel):
    address: str
    capacity: int
    opening_time: time
    closing_time: time

class CinemaHall(CinemaHallBase):
    opening_time: time
    closing_time: time

class CinemaHallDetailed(CinemaHallBase):
    opening_time: time
    closing_time: time
    seats: List[SeatBase]