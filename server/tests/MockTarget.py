from MockImage import MockImage

class MockTarget(object):
    def __init__(self, target_region_id, image=None, target_type=None,
                letter=None, letter_color=None, background_color=None,
                shape=None, orientation=None, notes=None, manual=None,
                coord1=None, coord2=None, width=None, height=None):
        self.target_region_id = target_region_id
        self.target_type = target_type
        self.letter = letter
        self.letter_color = letter_color
        self.background_color = background_color
        self.shape = shape
        self.orientation = orientation
        self.notes = notes
        self.coord1 = coord1
        self.coord2 = coord2

        self.target = self # This makes this object mock both ShimmerTarget and ARC.Target
        self.image = MockImage([self])

        from MockFlight import MockFlight
        self.flight = MockFlight(mock_directory=True)

    def delete_region(self):
        pass

    def update_thumbnail(self, thumbnail_path):
        pass
