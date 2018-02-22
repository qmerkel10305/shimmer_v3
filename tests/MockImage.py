class MockImage(object):
    def __init__(self, mock_targets):
        self.mock_targets = mock_targets

    def get_target_regions(self, flight=None):
        return self.mock_targets