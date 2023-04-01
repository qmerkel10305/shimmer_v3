from fastapi import APIRouter

from utils.queue import ShimmerQueue
from orm.schema import Image, CreateTarget
from utils.flight import CURRENT_FLIGHT


from orm.crud.image import delete_target_region, get_target_region, delete_target_region
from orm.crud.target import get_targets_near

router = APIRouter(prefix="/image")

image_model = ShimmerQueue(CURRENT_FLIGHT)

#next endpoint
@router.get('/next', response_model= Image)
async def get_next_image():
    return image_model.get_next_image()
#get image
@router.get('/<int:img_index>/', response_model = Image)
async def get_image(img_index: int):
    try:
        return image_model.get_image(img_index)
    except IndexError:
        raise HTTPException(status_code=404, detail="No image associated with that index")
#get image file
@router.get('/<int:img_index>/img.jpg', response_class = FileResponse)
async def get_image_file(img_index: int):
    img = image_model.img(img_index)
    return img.GetImagePath()

#get target region by image
@router.get("/<int:img_index>/region/<int:region_id>", response_model= TargetRegion)
async def getTargetRegion(img_index, region_id):
    img = image_model.img(img_index)
    get_target_region(db, CURRENT_FLIGHT.flight_id, img.image_id, region_id)
    
    
# delete target region by image
@router.delete("/<int:img_index>/region/<int:region_id>", response_model= TargetRegion)
async def deleteTargetRegion(img_index, region_id):
    img = image_model.img(img_index)
    region = delete_target_region(db, CURRENT_FLIGHT.flight_id,img.image_id, region_id)
    
    if len(get_target_regions(region.target_id, CURRENT_FLIGHT.flight_id, db)) == 0:
        delete_target(CURRENT_FLIGHT.flight_id, region.target_id, db)
    
    db.commit()

@router.post("/<int:idx>/target")
async def postTarget(image_dx, target, target_region):
	img = image_model.img(idx)
	# calculate ewkt string
	if target_region.bottom_right is None:
		ewkt_x = target_region.top_left.x
		ewkt_y = target_region.top_left.y
	else:
		ewkt_x = (target_region.top_left.x + target_region.bottom_right.x) / 2
		ewkt_y = (target_region.top_left.y +  target_region.bottom_right.y) / 2
	
    ewkt = f"SRID={CURRENT_FLIGHT.srid};MULTIPOINT({ewkt_x} {ewkt_y})"
 
    new_target = TargetCreate(**target.dict(), flight_id = CURRENT_FLIGHT.flight_id, ewkt)
    
	t = create_target(db, new_target, flight_id, target, ewkt, ...)

	if target_region.bottom_right is not None:
		region = crud.create_target_region(flight_id, target_region, t.target_id)
		thumb_path = create_region_thumbnail(region.id, t.target_id, flight_id)
		crud.update_target(thumbnail=thumb_path)

#get targets near

@router.get("/<int:img_index>/targets-near", response_model = List[models.Target])
async def getTargetsNear(img_index):
    img = image_model.img(img_index)
    x = float(request.args.get("x"))
    y = float(request.args.get("y"))
    distance = float(request.args.get("distance", 50))
    coord = img.coord(x, y, to_wgs84=False)
    
    
    targets = get_targets_near(coord, distance, db) #Doesn't exist
    if targets is None:
        abort(406)
    return targets