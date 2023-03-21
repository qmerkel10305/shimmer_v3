from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, UploadFile, File
from pyexiv2.metadata import ImageMetadata
from sqlalchemy.orm import Session

from orm.crud.image import create_image, get_new_image_id, update_image_file
from orm.database import get_db
from orm.schema import ImageCreate, ImageUpdate, Image
from utils.flight import CURRENT_FLIGHT
from utils.image import as_wkt, get_datetime, get_nadir

from .models import RequestInfo

router = APIRouter(prefix="/hades")


@router.post("/downlink", response_model=Image)
async def downlink(
    info: RequestInfo = Depends(),
    image: UploadFile = File(),
    db: Session = Depends(get_db),
):
    """
    Endpoint to downlink an image into the database.
    The image will be saved to disk and inserted inserted using form info from the request based on image type

    Args:
        info (RequestInfo, optional): Form info of the http request. Defaults to Depends().
        file (UploadFile, optional): The image to downlink. Defaults to File().
        db (Session, optional): The database to downlink into. Defaults to Depends(get_db).

    Returns:
        Image: The schema representing an image in the system, used to return the id of the image
    """
    current_flight_id = CURRENT_FLIGHT.flight_id
    image_id = get_new_image_id(db, current_flight_id)
    try:
        filename = f"flight_{current_flight_id}_im{image_id:05d}"
        if info.image_type == "low":
            filename += ".lowquality"
        if info.extension is not None:
            filename += f".{info.extension}"
        elif info.image_type == "low" or info.image_type == "high":
            filename += ".jpg"
        else:
            filename += ".png"
        output_path = Path(CURRENT_FLIGHT.root_folder).joinpath(filename)
        async with aiofiles.open(output_path, "wb") as f:
            content = await image.read()
            await f.write(content)
        # Check to make sure downlinked image is a valid file
        im = ImageMetadata(str(output_path.resolve()))
        im.read()
    except Exception as e:
        output_path.unlink(missing_ok=True)
        raise e

    if info.remote_id == None:
        ic = ImageCreate(
            flight_id=current_flight_id,
            date_time=get_datetime(im),
            nadir=get_nadir(im),
            geom=as_wkt(im),
        )
        if info.image_type == "low":
            ic.low_quality_jpg = filename
        elif info.image_type == "high":
            ic.high_quality_jpg = filename
        else:
            ic.path = filename
        return create_image(db, ic)
    else:
        iu = ImageUpdate(flight_id=current_flight_id, image_id=info.remote_id)
        if info.image_type == "low":
            iu.low_quality_jpg = filename
        elif info.image_type == "high":
            iu.high_quality_jpg = filename
        else:
            iu.path = filename
        return update_image_file(db, iu)
