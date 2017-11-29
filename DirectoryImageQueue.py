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

    def get_next_image(self):
        """
        Retrieves the next image out of the queue
        """
        try:
            return join(self.folder, self.queue.popleft())
        except IndexError:
            return None
