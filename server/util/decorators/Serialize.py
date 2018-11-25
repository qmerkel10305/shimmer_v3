import json
from functools import wraps
from enum import Enum

from server.util.JSONObject import JSONObject

class JsonEncoder(json.JSONEncoder):
    """
    JSON Encoder class for encoding data into JSON strings
    """
    def default(self, o):
        if isinstance(o, Exception):
            return o.__class__.__name__ + ": " + str(o)
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, JSONObject):
            return o.serialize()
        return super().default(o)

def serialize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return json.dumps(f(*args, **kwargs), cls=JsonEncoder)
    return decorated_function