import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from geoalchemy2 import Geometry

SQLALCHEMY_DATABASE_URL = URL.create(
    "postgresql",
    username="arcstandard",
    password="arc",
    host=os.getenv("ARC_DB_HOST", "localhost"),
    database="imagery",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Yield to create a new session to a database

    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
