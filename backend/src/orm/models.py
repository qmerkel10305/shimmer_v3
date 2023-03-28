from geoalchemy2 import Geometry
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from orm.database import Base


class Flight(Base):
    """
    Class representing a Flight in the database

    Inherits:
        Base (DeclarativeBase): SQLAlchemy DeclarativeBase for database
    
    Attributes:
        flight_id (int): The id of the flight. Primary Key
        root_folder (str): Root folder where all images are stored within. None by default.
        location (str): String representation of flight location
        srid (int): SRID of the flight location
        date_time (datetime): Datetime of the flight
        images (Image):  List of images associated with the flight
        targst (Target): List of targets associated with the flight
    """
    __tablename__ = "flights"

    flight_id = Column(Integer, primary_key=True)
    root_folder = Column(Text, nullable=True)
    location = Column(Text)
    srid = Column(Integer)
    date_time = Column(DateTime)

    images = relationship("Image", backref="flight")
    targets = relationship("Target", backref="flight")


class Image(Base):
    """
    Class representing an Image in the database

    Inherits:
        Base (DeclarativeBase): SQLAlchemy DeclarativeBase for database

    Attributes:
        image_id (int): The id of the image. Primary Key.
        flight_id (int): The flight id the image is apart of.
        path (str): The path to the original quality image.
        low_quality_jpg (str): The path to the low quality image. None by default. 
        high_quality_jpg (str): The path to the low quality image. None by Default.
        date_time (datetime): Datetime of the image
        nadir (bool): Boolean if the image is nadir or not
        geom (str): WKT string representing the image.
        targets (Target): List of targets associated with an image.
    """
    __tablename__ = "images"

    image_id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey("flights.flight_id"))
    path = Column(Text)
    low_quality_jpg = Column(Text, nullable=True)
    high_quality_jpg = Column(Text, nullable=True)
    date_time = Column(DateTime)
    nadir = Column(Boolean)
    geom = Column(Geometry("POLYGON"))

    targets = relationship("Target", backref="image")

    def GetImagePath(self) -> str:
        if self.Path is not "":
            return self.Path
        elif self.high_quality_jpg is not None:
            return self.high_quality_jpg
        elif self.low_quality_jpg is not None:
            return self.low_quality_jpg
        else:
            raise Exception("Image not found")
    
class Target(Base):
    """
    Class representing an Target in the database

    Inherits:
        Base (DeclarativeBase): SQLAlchemy DeclarativeBase for database

    Attributes:
        target_id (int): The id the target. Primary Key.
        target_type (str): The type of the target. None by default.
        image_id (int): The id of the image the target is associate with.
        flight_id (int): The flight id the target is apart of.
        letter (str): The letter of the target. None by default.
        shape (str): The shape of the target. None by default.
        background_color (str): The color of the background of the target. None by default
        letter_color (str): The color of the letter on the target. None by default
        orientation (int): Int representing the orientation of the target related to North. None by default
        notes (str): Notes associated with the target. None by default.
        geom (str): WKT string representing the target. 
        thumbnail (str): The path to the target thumbnail image. None by default
        manual (bool): Boolean to check if target was manually processed.
    """
    __tablename__ = "targets"

    target_id = Column(Integer, primary_key=True)
    target_type = Column(Text, nullable=True)
    image_id = Column(Integer, ForeignKey("images.image_id"))
    flight_id = Column(Integer, ForeignKey("flights.flight_id"))
    letter = Column(Text, nullable=True)
    shape = Column(Text, nullable=True)
    background_color = Column(Text, nullable=True)
    letter_color = Column(Text, nullable=True)
    orientation = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    geom = Column(Geometry("MULTIPOINT"))
    thumbnail = Column(Text, nullable=True)
    manual = Column(Boolean)


class TargetRegion(Base):
    """
    Class representing an Target Region in the database

    Inherits:
        Base (DeclarativeBase): SQLAlchemy DeclarativeBase for database

    Attributes:
        target_region_id (int): The id of the target region. Primary Key.
        flight_id (int): The flight id the target region is apart of.
        image_id (int): The image id the target region is apart of.
        target_id (int): The target id the target region is apart of.
        point1 (List[int, int]): Pixel value (x, y) representing the top left corner of the target
        point2 (List[int, int]): Pixel value (x, y) representing the bottom right corner of the target
    """
    __tablename__ = "target_regions"

    target_region_id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey("flights.flight_id"))
    image_id = Column(Integer, ForeignKey("images.image_id"))
    target_id = Column(Integer, ForeignKey("targets.target_id"))
    point1 = Column(ARRAY(Integer))
    point2 = Column(ARRAY(Integer))
    manual = Column(Boolean)
