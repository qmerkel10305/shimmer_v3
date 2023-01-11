import argparse
from datetime import datetime

from orm.crud.flight import create_flight
from orm.database import get_db
from orm.schema import FlightCreate
from utils.location import Location

if __name__ == "__main__":
    """
    Script to insert a new flight into the database, will create a new flight at the next availible number
    """
    parser = argparse.ArgumentParser(
        description="Inserts flight into database and creates folder."
    )
    parser.add_argument("-l", "--location", type=str, help="Flight location")
    parser.add_argument("-s", "--srid", type=int, help="Flight SRID")
    args = parser.parse_args()

    if args.location or args.srid:
        if not (args.location and args.srid):
            parser.error("Location and SRID must be specified")
        location = args.location
        srid = args.srid
    else:
        print("Presets:")
        for i, val in enumerate(Location.presets()):
            print("%d: '%s' (SRID: %d)" % (i, val.name, val.srid))
        try:
            choice = int(input("Select location #: "))
            choice = Location.presets()[choice]
            location = choice.name
            srid = choice.srid
        except:
            print("Bad selection")
            raise
    fc = FlightCreate(location=choice.name, srid=choice.srid, date_time=datetime.now())
    flight = create_flight(get_db(), fc)

    print("Flight ID: %d Directory: %s" % (flight.flight_id, flight.root_folder))
