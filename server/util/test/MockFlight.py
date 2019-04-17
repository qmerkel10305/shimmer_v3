import os
import tempfile
import atexit

from ARC.Flight import FlightCore

from server.util.test.MockImage import MockImage
from server.util.test.MockTarget import MockTarget
from server.util.test.MockTargetRegion import MockTargetRegion

class MockFlight(FlightCore):
    next_target_id = 1
    next_target_region_id = 1
    def __init__(self, images=[], targets=[], mock_directory=False):
        self.flight_id = 1
        self._images = images
        self._targets = targets
        if mock_directory:
            self.mock_dir = tempfile.TemporaryDirectory()
            self.folder = self.mock_dir.name
            os.mkdir(os.path.join(self.folder, "targets"))
            atexit.register(self.tempfile_cleanup)

    def image(self, image_id):
        for img in self._images:
            if img.image_id == image_id:
                return img
        raise ValueError("Not Found")

    def target(self, id):
        return self._targets[id]

    def all_targets(self):
        return [target for target in self._targets if not target._deleted]

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

    def insert_target(self, coord1, coord2=None, **kwargs):
        target = MockTarget(MockFlight.next_target_id, **kwargs)
        MockFlight.next_target_id += 1

        if coord2 is not None:
            target_region = MockTargetRegion(MockFlight.next_target_region_id, flight=self, coord1=coord1, coord2=coord2)
            target_region.image = MockImage([target_region])
            MockFlight.next_target_region_id += 1

            return target, target_region
        else:
            return target

class MockQuery(object):
    def __init__(self, values):
        self.values = values

    def one(self):
        return self.values[0]

    def all(self):
        return self.values