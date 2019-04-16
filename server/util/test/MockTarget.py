from server.util.test.MockImage import MockImage

class MockTarget(object):
    def __init__(self, target_id, image=None, target_type=None,
                letter=None, letter_color=None, shape_color=None,
                shape=None, orientation=None, notes=None, manual=None):
        self.target_id = target_id
        self.target_type = target_type
        self.letter = letter
        self.letter_color = letter_color
        self.background_color = shape_color
        self.shape = shape
        self.orientation = orientation
        self.notes = notes

        self.image = image
        self.flight = None