import json

from sqlalchemy.orm import Session

from orm import models, schema

from routers.target.models import PostTarget
from orm.models import GetImagePath
from utils.image import get_coord_from_img
from pyexiv2.metadata import ImageMetadata


def get_all_targets(db: Session, flight_id: int) -> List[models.Target]:
    return db.query(models.Target).filter(models.Flight.flight_id == flight_id).all()

def get_target(db: Session, flight_id: int, target_id: int) -> models.Target:
    return db.query(models.Target).filter(models.Flight.flight_id == flight_id).filter(models.Target.target_id == target_id).one()


def merge_targets(target_id: int, target_ids: List[int], flight_id: int, db: Session) -> models.Target:
    target = db.query(models.Target).filter(models.Flight.flight_id == flight_id).filter(models.Target.target_id == target_id).one()

    for t_id in target_ids:
        t_db = db.query(models.Target).filter(models.Flight.flight_id == flight_id).filter(models.Target.target_id == t_id).one()
        for tr in t_db.target_regions:
            # update tr.target_id in db to target_id
            tr.target_id = target.target_id
            # get image from db
            img = db.query(models.Image).filter(models.Flight.flight_id == flight_id).filter(tr.image_id).one()
            #get the metadata for the image
            img_path = img.GetImagePath()
            image_metadata = ImageMetadata(img_path)
            
            x1,y1 = get_coord_from_img(image_metadata, tr.point1[0], tr.point1[1], to_wgs84 = False)
            x2,x2 = get_coord_from_img(image_metadata, tr.point2[0], tr.point2[1], to_wgs84 = False)
            
            center = (x1 + x2)/2, (y1 + y2)/2
            
            ewkt = "SRID=%d;POINT(%f %f)" % (self.srid, center[0], center[1])
            tr.geom == tr.geom.ST_Union(ewkt)
            db.commit()
        delete_target(t_id, db)
    return target
    
def create_target(db: Session, target : CreateTarget) -> models.Target:
    db_target = models.Target(**target.dict())
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target
     
    
def delete_target(target_id: int, db: Session) -> models.Target:
    target = db.query(models.Target).filter(models.Flight.flight_id == flight_id).filter(models.Target.target_id == target_id).one()
    db.delete(target)
    db.commit()
    return target
    
def update_target(target: schema.TargetUpdate, db: Session) -> models.Target:
    db_target: models.Target = (db.query(models.Target).filter(
        models.Target.flight_id == target.flight_id,
        models.Target.target_id == target.target_id,
    ).one()        
    )
        
    if target.flight_id is not None:
        db_target.flight_id = target.flight_id
    if target.target_type is not None:
        db_target.target_type = target.target_type
    if target.letter is not None:
        db_target.letter = target.letter
    if target.shape is not None:
        db_target.shape = target.shape
    if target.background_color is not None:
        db_target.background_color = target.background_color
    if target.letter_color is not None:
        db_target.letter_color = target.letter_color
    if target.orientation is not None:
        db_target.orientation = target.orientation
    if target.target_id is not None:
        db_target.target_id = target.target_id
        
    db.commit()
    db.refresh(db_target)
    return db_target

def get_target_region(target_id : int, region_id : int,flight_id : int, db: Session) -> models.TargetRegion:
    return db.query(models.TargetRegion).filter(models.TargetRegion.flight_id == flight_id).filter(models.TargetRegion.target_id == target_id).filter(models.TargetRegion.target_region_id == region_id).one()

def get_target_regions(target_id : int, flight_id : int, db: Session) -> List[models.TargetRegion]:
    return db.query(models.TargetRegion).filter(models.TargetRegion.flight_id == flight_id).filter(models.TargetRegion.target_id == target_id).all()

def get_target_thumbnail(flight_id:int, target_id: int, db: Session ) -> models.Image.thumbnail:
    return db.query(models.Target).filter(models.TargetRegion.flight_id == flight_id).filter(models.TargetRegion.target_id == target_id).one()
