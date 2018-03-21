"""
Loads images from a directory
"""

import os
from os.path import join
from collections import deque
from ImageQueue import ImageQueue

class DirectoryImageQueue(ImageQueue):
    """
    A class for loading images from a flight.

    Arguments:
        folder: The directory to load images from
    """

    def __init__(self, folder):
        super(DirectoryImageQueue, self).__init__()
        self.folder = folder
        self.queue = deque(os.listdir(folder))
        self.flight = DirectoryFlight()

    def get_next_image(self):
        """
        Retrieves the next image out of the queue
        """
        try:
            return DirectoryImage(join(self.folder, self.queue.popleft()))
        except IndexError:
            return None

    def get_flight_id(self):
        """
        Returns the flight id associated with the queue
        """
        return 0

class DirectoryImage(object):
    """
    Image class for an image in a directory
    """
    def __init__(self, path):
        self.path = path

    def jpg(self):
        return self.path

    def get_target_regions(self, flight=None):
        return []

class DirectoryFlight(object):
    """
    Flight class for images in a directory
    """
    def __init__(self):
        self.flight_id = 0
        self.next_id = 0

    def insert_target(self, coord1, coord2, image, manual, target_type, letter, shape,
                      orientation, letter_color, background_color, notes):
        print "x: " + str(coord1[0]) + " y: " + str(coord1[1]) + "orientation: " + orientation
        print "letter: " + letter + " letter_color: " + letter_color
        print "shape: " + shape + " background_color: " + background_color
        self.next_id += 1
        return (None, self.next_id)
