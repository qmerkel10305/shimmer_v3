import json
from functools import wraps
from enum import Enum

class JsonEncoder(json.JSONEncoder):
    """
    JSON Encoder class for encoding data into JSON strings
    """
    def default(self, o):
        if isinstance(o, Exception):
            return o.__class__.__name__ + ": " + str(o)
        if isinstance(o, Enum):
            return o.value
        return dict(o)

def serialize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return json.dumps(f(*args, **kwargs), cls=JsonEncoder)
    return decorated_function