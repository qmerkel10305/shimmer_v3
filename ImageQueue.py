"""
An abstract class for queues of images
"""

class ImageQueue(object):
    """
    An abstract class for queues of images
    """

    def __init__(self):
        pass

    def get_next_image(self):
        """
        Retrieves the next image out of the queue
        """
        raise NotImplementedError("Image Queue subclasses implement get_next_image")

    def get_flight_id(self):
        """
        Returns the flight id associated with the queue
        """
        raise NotImplementedError("Image Queue subclasses implement get_flight_id")
