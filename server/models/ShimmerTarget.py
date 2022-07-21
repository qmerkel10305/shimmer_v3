from server.util.JSONObject import JSONObject
from server.models.ShimmerTargetRegion import ShimmerTargetRegion
import pyproj
import ARC


class ShimmerTarget(JSONObject):
    def __init__(self, target):
        self.target = target

    @property
    def id(self):
        return self.target.target_id

    def delete(self):
        regions = self.target.get_target_regions()
        for region in regions:
            target_region = ShimmerTargetRegion(region)
            target_region.delete_thumbnail()
            target_region.target_region.delete_region()

    ############################################################################
    ############################ JSONObject Methods ############################
    ############################################################################

    def serialize(self):
        return {
            "id": self.id,
            "target_type": self.target.target_type,
            "letter": self.target.letter,
            "shape": self.target.shape,
            "letter_color": self.target.letter_color,
            "shape_color": self.target.background_color,
            "orientation": self.target.orientation,
            "notes": self.target.notes,
            "manual": self.target.manual
        }

    def deserialize(self, new_target):
        if new_target["id"] != self.id:
            raise ValueError("Target ID does not match")
        if new_target["manual"] != True:
            raise ValueError("Only manual targets may be updated")

        self.target.update_target_type(int(new_target["target_type"]))
        self.target.update_letter(new_target["letter"])
        self.target.update_letter_color(new_target["letter_color"])
        self.target.update_shape(new_target["shape"])
        self.target.update_background_color(new_target["shape_color"])
        self.target.update_orientation(new_target["orientation"])
        self.target.update_notes(new_target["notes"])
        
    def serialize_interop(self):
        mission = 2

        directions = {'N': 0, 'NE': 45, 'E': 90, 'SE': 135,
              'S': 180, 'SW': 225, 'W': 270, 'NW': 315,
              'N': 360}

        def orientation2direction(orientation):
            min_dist = 360
            min_dir = None

            for direction, angle in directions.items():
                dist = abs(orientation-angle)
                if dist < min_dist:
                    min_dist = dist
                    min_dir = direction

            return min_dir

        x, y = self.target.coord
        target_projection = pyproj.Proj(init="epsg:%d" % self.target.srid)
        lon, lat = pyproj.transform(target_projection, ARC.presets.wgs84, x, y)
        shape = ARC.Shape[self.target.shape]
        shape_color = ARC.Color[self.target.background_color]
        letter_color = ARC.Color[self.target.letter_color]
        return {
            "type": (self.target.target_type.value if type(self.target.target_type) is ARC.TargetType else self.target.target_type) + 1,
            "mission": mission,
            "latitude": lat,
            "longitude": lon,
            "orientation": orientation2direction(self.target.orientation),
            "shape": shape.value + 1,
            "alphanumeric": self.target.letter,
            "shapeColor": shape_color.value + 1,
            "alphanumericColor": letter_color.value + 1,
            "description": self.target.notes,
            "autonomous": False
        }