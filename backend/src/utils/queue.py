from sqlalchemy.orm import Session
from orm.crud.image import get_all_images, get_image_by_id, get_images_after_time
from orm.models import Image

class ShimmerQueue(object):
    def __init__(self, flight_id: int) -> None:
        self.flight_id = flight_id
        self.replay_pos = 0
        self.current_pos = 0
        self.image_ids: list[int] = None

    def intialize_queue(self, db:Session) -> None:
        self.image_ids = [i.image_id for i in get_all_images(db, self.flight_id)]
    
    def update_queue(self, db:Session):
        latest_image = get_image_by_id(db, self.flight_id, self.image_ids[len(self.image_ids) - 1])
        self.image_ids.append(get_images_after_time(db ,self.flight_id, latest_image.date_time))

    def get_next_image(self, db: Session):
        if self.image_ids is None:
            self.intialize_queue(db)
        self.update_queue(db)
        if(self.current_pos == len(self.image_ids)):
            img = self.get_replay_image(db)
        else:
            img = get_image_by_id(db, self.flight_id, self.image_ids[self.current_pos])
            self.current_pos += 1
        return img
        

    def get_replay_image(self, db: Session) -> Image:
        if self.replay_pos >= self.current_pos:
            self.replay_pos = 0
        img = get_image_by_id(db, self.flight_id, self.image_ids[self.replay_pos])
        self.replay_pos += 1
        return img

    def img(self, idx, db: Session) -> Image:
        if self.image_ids is None:
            self.intialize_queue(db)
        self.update_queue(db)
        return get_image_by_id(db, self.flight_id, self.image_ids[idx])