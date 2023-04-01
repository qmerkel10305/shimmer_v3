from pathlib import Path

import cv2

def get_region_thumbnail(flight_folder:str, target_region_id:int) -> Path:
    region_path = Path(flight_folder).joinpath(f"/regions/region_{target_region_id}.jpg")
    if not region_path.exists():
        return None
    return region_path
          
    

def create_region_thumbnail(flight_folder:str, flight_id: int, target_id: int, target_region_id:int, db: Session) -> Path:
    tr = db.query(models.TargetRegion).filter(models.TargetRegion.flight_id == flight_id).filter(models.TargetRegion.target_id == target_id).filter(models.TargetRegion.target_id == target_id).filter(models.TargetRegion.target_region_id == target_region_id).one()
    img = db.query(models.Image).filter(models.Image.flight_id == flight_id).filter(models.Image.image_id == tr.image_id).one()
    tgtimage = cv2.imread(
        img, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION
    )
    x = (
    	(tr.coord2[0], tr.coord1[0])
        if tr.coord1[0] > tr.coord2[0]
        else (tr.coord1[0], tr.coord2[0])
    )
    y = (
        (tr.coord2[1], tr.coord1[1])
        if tr.coord1[1] > tr.coord2[1]
        else (tr.coord1[1], tr.coord2[1])
    )
    # Set coordinates for cropped image
    crop_img = tgtimage[int(y[0]) : int(y[1]), int(x[0]) : int(x[1])]
    # Save the cropped image
    region_path = Path(flight_folder).joinpath(f"/regions/region_{target_region_id}.jpg")
    cv2.imwrite(region_path, crop_img)

    return region_path
    