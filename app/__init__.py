from app.database import engine, Base
from app.models.cinema_hall import CinemaHall
from app.models.seat import Seat
from app.models.film import Film
from app.models.screening import Screening
from app.models.booking import Booking
import logging


def initialize_database():
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    from app.models import cinema_hall, seat, film, screening, booking

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    created_tables = Base.metadata.tables.keys()
    print(f"Tables created: {list(created_tables)}")

    if not created_tables:
        raise RuntimeError("No tables were created!")


if __name__ == "__main__":
    initialize_database()