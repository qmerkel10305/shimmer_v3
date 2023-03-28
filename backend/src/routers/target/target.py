from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, Session
from orm.database import get_db
from orm.schema import Target, TargetCreate, TargetUpdate
from orm.crud.target import get_all_targets,get_target,merge_targets, delete_target, get_target_region, get_target_regions, update_target
from .models import PostTarget
from utils.region import get_region_thumbnail, create_region_thumbnail
from utils.flight import CURRENT_FLIGHT



router = APIRouter(prefix="/target")




@router.get('/', response_model = List[Target])
async def get_all_targets(db: Session = Depends(get_db)):
    """
    Call to the database to get all targets for a specific flight
    
    Args: 
        db(Session, optional): The database called for the target request. Defaults to Depends(get_db).
        
    Returns:
        List[Target]: List of Target objects
        Target: the schema representing the targets in the system, used to return the target
    """
    return get_all_targets(db, CURRENT_FLIGHT.flight_id)

@router.get('/<int:target_id>/', response_model = Target)
async def get_target(db: Session = Depends(get_db), target_id = 0):
    """
    Calls to the database and returns a specific Models.Target with the 
    specified target id
    
    Args: 
        db(Session, optional): The database called for the target request. Defaults to Depends(get_db).
        target_id (int,optional): The id number associated with the target. Defaults to 0.
        
    Returns:
        Target: the schema representing the targets in the system, used to return the target
    
    """
    return get_target(db, CURRENT_FLIGHT.flight_id, target_id)
    
@router.put('/',response_model = Target)
async def put_target(target = RequestTarget, db: Session = Depends(get_db)):
    tu = UpdateTarget(**target.dict())
    return update_target(tu, db)

@router.get('/merge/<int:target_id>/', response_model = Target)
async def mergeTargets(target_id:int, target_ids: List[int],db: Session = Depends(get_db)):
    return merge_targets(target_id, target_ids, CURRENT_FLIGHT.flight_id, db)
    

@router.get('/delete/<int:target_id>', response_model = Target)
async def deleteTarget(target_id : int, db: Session = Depends(get_db)):
    # Delete target w/ targetID
    return delete_target(target_id, db)

@router.get('/post/<int:target_id>', response_model = Target)
async def postTarget(target : PostTarget,  db: Session = Depends(get_db)):
    tc = TargetCreate(**target.dict(), flight_id = CURRENT_FLIGHT.flight_id,)
    
    # update with target region creation before returning
    return create_target(tc) 

@router.get('/<int:id>/thumb.jpg', response_class = FileResponse)
async def getTargetThumbnail(target_id: int, db: Session = Depends(get_db)):
    target = get_target(db, CURRENT_FLIGHT.flight_id, target_id)
    return target.thumbnail # if FastAPI automatically handles exceptions, otherwise fix

@router.get('/<int:target_id>/regions/<int:region_id>/thumb.jpg', response_class = FileResponse)
async def getRegionThumbnail(target_id: int, region_id: int, db: Session = Depends(get_db)):
    # return the thumbnail of the image given the imageID and regionID
    flight_folder = Path("")
    file = get_region_thumbnail(flight_folder, region_id)
    if file is None:
        file = create_region_thumbnail(flight_folder, CURRENT_FLIGHT.flight_id, target_id, region_id)
    return file
@router.get('/<int:target_id>/regions', response_class = FileResponse)
async def getTargetRegions(target_id: int,  db: Session = Depends(get_db)):
    return get_target_regions(target_id, region_id, CURRENT_FLIGHT.flight_id, db)


@router.get('/<int:target_id>/regions/update/<int:region_id>/', response_model = Target)
async def updateRegionThumbnail(target_id: int, region_id: int, db : Session = Depends(get_db)):
    thumb_path = get_region_thumbnail(CURRENT_FLIGHT.root_folder,region_id)
    if thumb_path is None:
        raise HTTPException(status_code=404, detail="Cannot set thumbnail to non existent image")
    return update_target(target_id,CURRENT_FLIGHT.root_folder,db)