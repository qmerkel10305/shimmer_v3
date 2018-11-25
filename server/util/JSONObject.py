class JSONObject(object):
    def serialize(self):
        """
        Return a dictionary representation of the object
        """
        raise NotImplementedError("Must be implemented by subtype")

    def deserialize(self, json_data):
        """
        Set this object's attributes based on json_data
        """
        raise NotImplementedError("Must be implemented by subtype")