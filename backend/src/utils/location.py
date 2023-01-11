from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from pyproj import Proj


@dataclass
class Location:
    name: str
    projection: Proj
    srid: int
    ground_elevation: float
    bounds: Tuple[Tuple[int, int]]
    """
    Describes the general location an image was taken.
    This dataclass provides context for the area an image
    was taken, allowing various aspects of the telemetry to be interpreted
    appropriately.
    A location can be an area of any size, so long as the given parameters are
    reasonably accurate over the entire area.

    Attributes:
        name (str):
            Human-readable description of this location
        projection (Proj):
            Proj object of the
            UTM (Universal Transverse Mercator) projection to use for
            this location.
        srid (int):
            SRID of the projection used in this area.
        ground_elevation:
            Elevation of the ground above the reference geoid for this
            location.
        bounds (Tuple[Tuple[int, int]]):
            Bounding box of area, in WGS84 decimal coordinates.  In the form
            `((min lat, min lon), (max lat, max lon))`.
    """

    @staticmethod
    def presets() -> List[Location]:
        """
        Return a list of predefined locations

        Returns:
            List[Location]: List of Locations
        """
        return [
            Location(
                name="Perkins Field, Butner, NC",
                projection=Proj("epsg:32617"),  # UTM Zone 17N
                srid=32617,
                ground_elevation=107.1,  # (m) (350ft)
                bounds=((36.158869, -78.813654), (36.177000, -78.790000)),
            ),
            Location(
                name="Webster Field Annex, St. Inigoes, MD",
                projection=Proj("epsg:32618"),  # UTM Zone 18N
                srid=32618,
                # (m) *VERY ROUGH ESTIMATE* (Geoid -36.1m + 15ft MSL)
                ground_elevation=-31.58,
                # Greater southern Maryland area
                bounds=((38.026338, -76.522979), (38.317719, -76.323849)),
            ),
            Location(
                name="NCSU, Raleigh, NC",
                projection=Proj("epsg:32617"),  # UTM Zone 17N
                srid=32617,
                ground_elevation=115.8,  # (m) (380ft in the Oval)
                bounds=((35.714589, -78.717550), (35.789876, -78.631281)),
            ),
            Location(
                name="RDRC",
                projection=Proj("epsg:32617"),  # UTM Zone 17N,
                srid=32617,
                ground_elevation=112.8,  # (m) (370ft)
                bounds=((35.945104, -78.356812), (35.938920, -78.346799)),
            ),
            Location(
                name="Wayne",
                projection=Proj("epsg:32617"),  # UTM Zone 17N,
                srid=32617,
                ground_elevation=53.75,  # (m) (370ft)
                bounds=((35.336825, -78.120689), (35.343818, -78.113115)),
            ),
            Location(
                name="St Mary's",
                projection=Proj("epsg:32618"),  # UTM Zone 18N
                srid=32618,
                ground_elevation=-31.58,
                bounds=((38.3077530, -76.5591717), (38.3234777, -76.5359545)),
            ),
        ]

    @staticmethod
    def get_location(lat: float, lon: float) -> Location:
        """
        Check to see if a point is within a predefined location

        Args:
            lat (float): The latitude of the point
            lon (float): The longitude of the point

        Raises:
            AttributeError: Unknown Location, please specify

        Returns:
            Location: Location containing the specified point
        """
        for loc in Location.presets():
            min_lat = loc.bounds[0][0]
            min_lon = loc.bounds[0][1]
            max_lat = loc.bounds[1][0]
            max_lon = loc.bounds[1][1]
            if lat >= min_lat and lat <= max_lat and lon >= min_lon and lon <= max_lon:
                return loc
        raise AttributeError("Unknown location, please specify.")
