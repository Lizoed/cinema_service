from pydantic import BaseModel
from uuid import UUID

class BookingCreate(BaseModel):
    screening_id: UUID
    seat_id: UUID
    client_name: str

class Booking(BaseModel):
    id: UUID
    screening_id: UUID
    seat_id: UUID
    client_name: str

    class Config:
        from_attributes = True