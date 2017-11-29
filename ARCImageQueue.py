"""
Loads images from an ARC.Flight
"""

from collections import deque
from ImageQueue import ImageQueue
import ARC

class ARCImageQueue(ImageQueue):
    """
    A class for loading images from a flight.

    Arguments:
        flight: The id of the flight to load from
    """

    def __init__(self, flight):
        super(ARCImageQueue, self).__init__()
        self.flight = ARC.Flight(flight)
        self.queue = deque(self.flight.all_images(filenames=True))
        self.flight.start_listener()

    def get_next_image(self):
        """
        Retrieves the next image out of the queue
        """
        img = self.flight.next_image(timeout=0.01, filename=True)
        if img:
            self.queue.append(img)

        try:
            return self.queue.popleft()
        except IndexError:
            return None
