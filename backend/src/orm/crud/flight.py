from pathlib import Path

from sqlalchemy.orm import Session

from orm import models, schema

BASE_FOLDER = Path("/RAID/Imagery/")


def get_flight_by_id(db: Session, flight_id: int) -> models.Flight:
    """
    Gets a flight object by id from the database

    Args:
        db (Session): The database session
        flight_id (int): The flight id to obtain

    Returns:
        models.Flight: Flight with the id submitted
    """
    return db.query(models.Flight).filter(models.Flight.flight_id == flight_id).one()


def create_flight(
    db: Session, flight: schema.FlightCreate, flight_id: int = None
) -> models.Flight:
    """
    Creates a new flight in the database

    Args:
        db (Session): The database session
        flight (schema.FlightCreate): The schema for flight creation
        flight_id (int, optional): A specified flight id to create. Defaults to None.

    Returns:
        models.Flight: The created flight object
    """
    db_flight = models.Flight(**flight.dict())
    if flight_id is not None:
        db_flight.flight_id = flight_id
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)

    flight_dir = BASE_FOLDER.joinpath(f"Flight_{db_flight.flight_id}")
    flight_dir.mkdir(parents=True, exist_ok=True)
    flight_dir.joinpath("targets").mkdir(exist_ok=True)
    flight_dir.joinpath("regions").mkdir(exist_ok=True)

    db_flight.root_folder = str(flight_dir.resolve())
    db.commit()
    return db_flight
