import cv2
import os

from server.util.JSONObject import JSONObject


class ShimmerTargetRegion(JSONObject):
    def __init__(self, target_region):
        self.target_region = target_region
        self.thumbnail_path = self.get_thumbnail_if_exists()

    @property
    def id(self):
        return self.target_region.target_region_id

    def create_thumbnail(self):
        tgtimage = self.target_region.image.jpg()

        tgtimage = cv2.imread(tgtimage, cv2.IMREAD_COLOR |
                              cv2.IMREAD_IGNORE_ORIENTATION)
        # Set coordinates for cropped image
        crop_img = tgtimage[int(self.target_region.coord1[1]):int(self.target_region.coord2[1]),
                            int(self.target_region.coord1[0]):int(self.target_region.coord2[0])]
        # Save the cropped image
        region_path = self.target_region.flight.folder + "/regions/region_" + \
            str(self.target_region.target_region_id) + ".jpg"
        target_path = self.target_region.flight.folder + "/targets/target_" + \
            str(self.target_region.target_region_id) + ".jpg"
        cv2.imwrite(region_path, crop_img)
        os.symlink(region_path, target_path)
        self.target_region.target.update_thumbnail(target_path)

    def get_thumbnail_if_exists(self):
        thumbnail_path = self.target_region.flight.folder + "/regions/region_" + \
            str(self.target_region.target_region_id) + ".jpg"
        if not os.path.exists(thumbnail_path):
            self.create_thumbnail()
        return thumbnail_path

    def delete_thumbnail(self):
        if self.thumbnail_path and os.path.exists(self.thumbnail_path):
            os.remove(self.thumbnail_path)
            

    ############################################################################
    ############################ JSONObject Methods ############################
    ############################################################################

    def serialize(self):
        return {
            'id': self.id,
            'target_id': self.target_region.target.target_id,
            'image_id': self.target_region.image.image_id,
            'a': {'x': self.target_region.coord1[0], 'y': self.target_region.coord1[1]},
            'b': {'x': self.target_region.coord2[0], 'y': self.target_region.coord2[1]},
        }

    def deserialize(self, json_data):
        new_target = json_data
        if new_target['id'] != self.id:
            raise ValueError("Target Region ID does not match")

        if new_target['target_id'] != self.target_region.target.target_id:
            raise ValueError("Target Region Target ID does not match")

        if new_target['image_id'] != self.target_region.image.image_id:
            raise ValueError("Target Region Image ID does not match")

        raise NotImplementedError(
            "Deserializing and editing target region values is not supported")
