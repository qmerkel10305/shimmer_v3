from functools import wraps
from collections import deque

import server.models.GlobalModel as GlobalModel

from server.ImageQueue import ImageQueue
from server.models.ShimmerModel import ShimmerModel

from server.util.test.MockImage import MockImage
from server.util.test.MockFlight import MockFlight

def with_mock_model(images=[], targets=[]):
    def with_mock_model_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            GlobalModel.model = ShimmerModel(MockQueue(images, targets))
            f(*args, **kwargs)
            GlobalModel.model = None
        return decorated_function
    return with_mock_model_decorator

class MockQueue(ImageQueue):
    def __init__(self, images, targets):
        self.flight = MockFlight(images=images, targets=targets)
        self.queue = deque(images)

    def get_next_image(self):
        """
        Retrieves the next image out of the queue
        """
        try:
            return self.queue.popleft()
        except IndexError:
            return None

    def get_flight_id(self):
        """
        Returns the flight id associated with the queue
        """
        return 0
