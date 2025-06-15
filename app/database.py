from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.models.base import Base
import time
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@cinema_db:5432/cinema_db?client_encoding=utf8"

def wait_for_db():
    max_retries = 10
    for attempt in range(max_retries):
        try:
            engine = create_engine(
                SQLALCHEMY_DATABASE_URL,
                pool_pre_ping=True,
                connect_args={"options": "-c timezone=utc"}
            )
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return engine
        except OperationalError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2)

engine = wait_for_db()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)