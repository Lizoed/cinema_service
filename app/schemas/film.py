from pydantic import BaseModel
from uuid import UUID
from app.schemas.base import BaseSchema

class FilmBase(BaseSchema):
    id: UUID
    name: str
    duration: int

class FilmCreate(BaseModel):
    name: str
    duration: int

class Film(FilmBase):
    is_active: bool

class FilmWithStatus(FilmBase):
    is_active: bool