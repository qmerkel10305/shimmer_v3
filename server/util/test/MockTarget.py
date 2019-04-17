import os

from server.util.test.MockImage import MockImage

class MockTarget(object):
    def __init__(self, target_id, image=None, target_type=None, letter=None,
                letter_color=None, shape_color=None, shape=None,
                orientation=None, notes=None, manual=None, thumbnail=None,
                target_regions=[]):
        self.target_id = target_id
        self.target_type = target_type
        self.letter = letter
        self.letter_color = letter_color
        self.background_color = shape_color
        self.shape = shape
        self.orientation = orientation
        self.notes = notes
        self.manual = manual

        self.target_regions = target_regions
        self.image = image
        self.flight = None

        if thumbnail is None:
            self.thumbnail = os.path.abspath(os.path.join(__file__, os.pardir, "res", "target01.jpg"))
        else:
            self.thumbnail = thumbnail

        self._deleted = False

    def update_target_type(self, value):
        self.target_type = value

    def update_letter(self, value):
        self.letter = value

    def update_shape(self, value):
        self.shape = value

    def update_orientation(self, value):
        self.orientation = value

    def update_letter_color(self, value):
        self.letter_color = value

    def update_background_color(self, value):
        self.background_color = value

    def update_notes(self, value):
        self.notes = value

    def update_thumbnail(self, value):
        self.thumbnail = value

    def get_target_regions(self):
        return self.target_regions

    def delete_target(self):
        self._deleted = True

    def absorb_target(self, target):
        target.delete_target()
