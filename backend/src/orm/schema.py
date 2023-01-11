from datetime import datetime
from typing import List, Union

from pydantic import BaseModel

# Create database schema for return objects, replaces serialization done in shimmer 1


class ImageBase(BaseModel):
    """
    Class representing a image in the database with minimal information

    Inherits:
        BaseModel: Pydantic BaseModel
    
    Attributes:
        flight_id (int): The flight id of the image
        path (str): The path the original image on disk
        low_quality_jpg (Union[str, None]): The path for the low quality image on disk. Defaults to None
        high_quality_jpg (Union[str, None]): The path for the high quality image on disk. Defaults to None
    """
    flight_id: int
    path: str = ""
    low_quality_jpg: Union[str, None] = None
    high_quality_jpg: Union[str, None] = None


class ImageCreate(ImageBase):
    """
    Class representing information needed to create a new image in the database

    Inherits:
        ImageBase
    
    Attributes:
        date_time (datetime): The datetime when the image was taken.
        nadir (bool): Boolean if the image is nadir or not.
        geom (str): WKT string representing the image.
    """
    date_time: datetime
    nadir: bool
    geom: str


class ImageUpdate(ImageBase):
    """
    Class representing information needed to update a new image in the database

    Inherits:
        ImageBase
    
    Attributes:
        image_id (int): The id of the image in the database to update.
    """
    image_id: int


class Image(ImageUpdate, ImageCreate):
    """
    Class representing information about an image stored in the database

    Inherits:
        ImageUpdate
        ImageCreate
    """
    class Config:
        orm_mode = True


class FlightBase(BaseModel):
    """
    Class representing basic information about a flight

    Inherits:
        BaseModel: Pydantic BaseModel
    
    Attributes:
        date_time (datetime): The datetime when the image was taken.
        location (str): String Representation of a flight location
        srid (int): SRID of the flight location
    """
    location: str
    srid: int
    date_time: datetime


class FlightCreate(FlightBase):
    """
    Class representing information needed to create a new flight in the database

    Inherits:
        FlightBase
    """
    pass


class Flight(FlightCreate):
    """
    Class representing information about a flight in a database

    Inherits:
        FlightBase
    
    Attributes:
        flight_id (int): The id number of the flight
        root_folder (str): The root folder where all image are stored on disk
        images (List[Image]): List of images contained in the flight
    """
    flight_id: int
    root_folder: str
    images: List[Image]

    class Config:
        orm_mode = True
