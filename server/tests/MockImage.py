import os

class MockImage(object):
    def __init__(self, mock_targets):
        self.mock_targets = mock_targets

    def get_target_regions(self, flight=None):
        return self.mock_targets

    def jpg(self):
        return os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "res", "img0.jpg")