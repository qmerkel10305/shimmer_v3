from server.util.JSONObject import JSONObject

class ShimmerTarget(JSONObject):
    def __init__(self, target):
        self.target = target

    @property
    def id(self):
        return self.target.target_id

    def delete(self):
        regions = self.target.get_target_regions()
        for region in regions:
            region.delete_region()
        self.target.delete_target()

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

        self.target.update_target_type(new_target["target_type"])
        self.target.update_letter(new_target["letter"])
        self.target.update_letter_color(new_target["letter_color"])
        self.target.update_shape(new_target["shape"])
        self.target.update_background_color(new_target["shape_color"])
        self.target.update_orientation(new_target["orientation"])
        self.target.update_notes(new_target["notes"])