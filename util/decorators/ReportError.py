import logging

from enum import Enum
from functools import wraps

logger = logging.getLogger(__name__)

class StatusMessage(object):
    """
    Defines a message with a status indicator to be sent to the front end.
    """
    def __init__(self, val=None, e=None):
        if e is not None:
            self.status = "error"
        else:
            self.status = "okay"

        self.error = e
        self.data = val

    def __iter__(self):
        yield ('status', self.status)
        yield ('error', self.error)
        yield ('data', self.data)

def error(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        message = None
        try:
            val = f(*args, **kwargs)
            if val is not None:
                message = StatusMessage(val=val)
            else:
                message = StatusMessage()
        except Exception as e:
            logger.exception(e)
            message = StatusMessage(e=e)
        finally:
            return message
    return decorated_function