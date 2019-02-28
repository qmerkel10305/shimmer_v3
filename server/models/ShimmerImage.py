from server.models.ShimmerTarget import ShimmerTarget
from server.models.ShimmerTargetRegion import ShimmerTargetRegion

from server.util.JSONObject import JSONObject

class ShimmerImage(JSONObject):
    next_id = 0
    """
    ShimmerImage wraps data for an image.

    Arguments:
        image: the ARC.Image this ShimmerImage wraps
        flight: the ARC.Flight this image belongs to
    """
    def __init__(self, image, flight):
        self.image = image
        self.flight = flight

        self.id = ShimmerImage.next_id
        self.targets = [ ShimmerTargetRegion(tgt) for tgt in image.get_target_regions(flight=flight) ]

        ShimmerImage.next_id += 1

    @property
    def path(self):
        return self.image.jpg()

    def delete_region(self, i):
        self.targets[i].target_region.delete_region()
        del self.targets[i]

    def update(self):
        self. image = self.flight.image(self.image.image_id)
        self.targets = [ ShimmerTargetRegion(tgt) for tgt in self.image.get_target_regions(flight=self.flight) ]

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