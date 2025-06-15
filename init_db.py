import logging
from sqlalchemy import text
from app.database import engine, Base
from app.models import *

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def initialize_database():
    print("Checking database connection...")
    with engine.connect() as conn:
        conn.execute(text("SET search_path TO public"))
        version = conn.scalar(text("SELECT version()"))
        print(f"Connected to: {version}")

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        conn.execute(text("SET search_path TO public"))
        tables = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)).fetchall()
        print("Tables in database:", [t[0] for t in tables])


if __name__ == "__main__":
    initialize_database()