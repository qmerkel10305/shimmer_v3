import os

from orm.crud.flight import get_flight_by_id
from orm.database import get_db

CURRENT_FLIGHT = get_flight_by_id(next(get_db()), int(os.environ["ARC_FLIGHT"]))
