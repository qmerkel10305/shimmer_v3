from typing import Union
from typing import Literal
from typing import Optional

from pydantic import BaseModel


class RequestInfo(BaseModel):
    """
    Class representing the request form info for a hades incoming request

    Inherits:
        BaseModel: Pydantic BaseModel

    Attributes:
        image_type (Literal["low", "high", "orig"]): The image type of the downlinked image
        remote_id (Optional[int]): The remote_id of the image downlinked.
            If given, will update an image in the database instead of create. Defaults to None
        extension (Optional[str]): The file extension of the image. Defaults to None
    """

    image_type: Literal["low", "high", "orig"]
    remote_id: Optional[int] = None
    extension: Optional[str] = None
