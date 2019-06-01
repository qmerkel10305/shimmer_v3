import os

class MockImage(object):
    def __init__(self, mock_targets, image_id=1):
        self.image_id = image_id
        self.mock_targets = mock_targets

    def get_target_regions(self, flight=None):
        for tr in self.mock_targets:
            tr.flight = flight
        return self.mock_targets

    def jpg(self):
        return os.path.abspath(os.path.join(__file__, os.pardir, "res", "img0.jpg"))