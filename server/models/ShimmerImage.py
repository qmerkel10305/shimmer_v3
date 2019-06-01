from server.models.ShimmerTarget import ShimmerTarget
from server.models.ShimmerTargetRegion import ShimmerTargetRegion

from server.util.JSONObject import JSONObject

class ShimmerImage(JSONObject):
    """
    ShimmerImage wraps data for an image.

    Arguments:
        id: the local Shimmer ID of the image
        image: the ARC.Image this ShimmerImage wraps
        flight: the ARC.Flight this image belongs to
    """
    def __init__(self, id, image, flight):
        self.id = id
        self.image = image
        self.flight = flight

        self.targets = [ ShimmerTargetRegion(tgt) for tgt in image.get_target_regions(flight=flight) ]

    @property
    def path(self):
        return self.image.jpg()

    def delete_region(self, i):
        self.targets[i].target_region.delete_region()
        del self.targets[i]

    def add_target(self, image_id=None, target_id=None, target_type=None,
                   letter=None, letter_color=None, shape_color=None, shape=None,
                   orientation=None, notes=None, coord=None):
        return self.flight.insert_target(
            coord, image=self.image, manual=True,
            target_type=target_type, letter=letter, shape=shape,
            orientation=orientation, letter_color=letter_color,
            background_color=shape_color, notes=notes
        )

    def get_target_regions(self):
        return self.targets

    ############################################################################
    ############################ JSONObject Methods ############################
    ############################################################################

    def serialize(self):
        return {
            "id": self.id,
            "targets": [ target.serialize() for target in self.targets ],
            "flight": self.flight.flight_id
        }

    def deserialize(self, json_data):
        new_image = json_data
        if new_image['id'] != self.id:
            raise ValueError("Target Region ID does not match")

        raise NotImplementedError("Deserializing and editing target values is not supported")