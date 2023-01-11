from sqlalchemy.orm import Session

from orm import models, schema


def create_image(db: Session, image: schema.ImageCreate) -> models.Image:
    """
    Function to create a new image in the database

    Args:
        db (Session): The database to create the image in.
        image (schema.ImageCreate): Schema for an image

    Returns:
        models.Image: The created database image
    """
    db_image = models.Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def update_image_file(db: Session, image: schema.ImageUpdate) -> models.Image:
    """
    Function to update the image path of an image. Check which paths are submitted and update the newest one.

    Args:
        db (Session): The database to update the image in.
        image (schema.ImageUpdate): Schema for image update

    Returns:
        models.Image: The updated database image
    """
    db_image: models.Image = (
        db.query(models.Image)
        .filter(
            models.Image.flight_id == image.flight_id,
            models.Image.image_id == image.image_id,
        )
        .one()
    )
    if image.low_quality_jpg is not None:
        db_image.low_quality_jpg = image.low_quality_jpg
    elif image.high_quality_jpg is not None:
        db_image.high_quality_jpg = image.high_quality_jpg
    else:
        db_image.path = image.path
    db.commit()
    return db_image


def get_new_image_id(db: Session, flight_id: int) -> int:
    """
    Gets the next image id to be created. Picks the next one in sequence incrementally.

    Args:
        db (Session): The database session.
        flight_id (int): The flight id to search in

    Returns:
        int: The next image id
    """
    return len(db.query(models.Image).filter(models.Image.flight_id == flight_id).all())
