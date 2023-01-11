from typing import Union
from typing import Literal

from pydantic import BaseModel


class RequestInfo(BaseModel):
    """
    Class representing the request form info for a hades incoming request

    Inherits:
        BaseModel: Pydantic BaseModel
    
    Attributes:
        image_type (Literal["low", "high", "orig"]): The image type of the downlinked image
        remote_id (Union[int, None]): The remote_id of the image downlinked. 
            If given, will update an image in the database instead of create. Defaults to None
        extension (Union[str, None]): The file extension of the image. Defaults to None
    """
    image_type: Literal["low", "high", "orig"]
    remote_id: Union[int, None] = None
    extension: Union[str, None] = None
