from server.util.JSONObject import JSONObject

class ShimmerTarget(JSONObject):
    def __init__(self, target):
        self.target = target

    @property
    def id(self):
        return self.target.target_id

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
            "shape_color": self.target.shape_color,
            "orientation": self.target.orientation,
            "notes": self.target.notes
        }

    def deserialize(self, json_data):
        new_target = json_data
        if new_target['id'] != self.id:
            raise ValueError("Target Region ID does not match")

        raise NotImplementedError("Deserializing and editing target values is not supported")