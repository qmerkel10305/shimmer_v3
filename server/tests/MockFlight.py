import os
import tempfile
import atexit

from ARC.Flight import FlightCore

from MockTarget import MockTarget

class MockFlight(FlightCore):
    next_target_id = 1
    def __init__(self, mock_directory=False):
        if mock_directory:
            self.mock_dir = tempfile.TemporaryDirectory()
            self.folder = self.mock_dir.name
            os.mkdir(os.path.join(self.folder, "targets"))
            atexit.register(self.tempfile_cleanup)

    def tempfile_cleanup(self):
        self.mock_dir.cleanup()

    def prepare_target(self, target):
        pass

    def prepare_image(self, image):
        pass

    def query_targets(self, session, manual=None):
        return MockQuery([])

    def query_images(self, session):
        return MockQuery([])

    def insert_target(self, coord1, coord2, **kwargs):
        next_id = MockFlight.next_target_id
        MockFlight.next_target_id += 1
        return None, MockTarget(next_id, coord1=coord1, coord2=coord2, **kwargs)

class MockQuery(object):
    def __init__(self, values):
        self.values = values

    def one(self):
        return self.values[0]

    def all(self):
        return self.values