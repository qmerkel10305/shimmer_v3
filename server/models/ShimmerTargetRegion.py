import cv2

from server.util.JSONObject import JSONObject


class ShimmerTargetRegion(JSONObject):
    def __init__(self, target_region):
        self.target_region = target_region

    @property
    def id(self):
        return self.target_region.target_region_id

    def create_thumbnail(self):
        tgtimage = self.target_region.image.jpg()

        tgtimage = cv2.imread(
            tgtimage, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION
        )
        # Check to make sure coords are in correct order
        x = (
            (self.target_region.coord2[0], self.target_region.coord1[0])
            if self.target_region.coord1[0] > self.target_region.coord2[0]
            else (self.target_region.coord1[0], self.target_region.coord2[0])
        )
        y = (
            (self.target_region.coord2[1], self.target_region.coord1[1])
            if self.target_region.coord1[1] > self.target_region.coord2[1]
            else (self.target_region.coord1[1], self.target_region.coord2[1])
        )
        # Set coordinates for cropped image
        crop_img = tgtimage[int(y[0]) : int(y[1]), int(x[0]) : int(x[1])]
        # Save the cropped image
        thumbnail_path = (
            self.target_region.flight.folder
            + "/targets/target_"
            + str(self.target_region.target_region_id)
            + ".jpg"
        )
        cv2.imwrite(thumbnail_path, crop_img)
        self.target_region.target.update_thumbnail(thumbnail_path)

    def check_corners(self):
        return (
            self.target_region.coord1[1] > self.target_region.coord2[1]
            or self.target_region.coord1[0] > self.target_region.coord2[0]
        )

    ############################################################################
    ############################ JSONObject Methods ############################
    ############################################################################

    def serialize(self):
        return {
            "id": self.id,
            "target_id": self.target_region.target.target_id,
            "image_id": self.target_region.image.image_id,
            "a": {"x": self.target_region.coord1[0], "y": self.target_region.coord1[1]},
            "b": {"x": self.target_region.coord2[0], "y": self.target_region.coord2[1]},
        }

    def deserialize(self, json_data):
        new_target = json_data
        if new_target["id"] != self.id:
            raise ValueError("Target Region ID does not match")

        if new_target["target_id"] != self.target_region.target.target_id:
            raise ValueError("Target Region Target ID does not match")

        if new_target["image_id"] != self.target_region.image.image_id:
            raise ValueError("Target Region Image ID does not match")

        raise NotImplementedError(
            "Deserializing and editing target region values is not supported"
        )
