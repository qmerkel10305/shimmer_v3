from datetime import datetime

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from orm.crud.flight import create_flight, get_flight_by_id
from orm.schema import FlightCreate
from utils.location import Location

def create_test_data(db: Session):
    """
    Function to create test flights in database

    Args:
        db (Session): The database to create flights in
    """
    for i, l in enumerate(Location.presets(), start=1):
        try:
            get_flight_by_id(db, -i)
        except NoResultFound:
            fc = FlightCreate(location=l.name, srid=l.srid, date_time=datetime.now())
            create_flight(db, fc, flight_id=-i)
