class MockTarget(object):
    def __init__(self, target_region_id, image=None, target_type=None, letter=None,
                   letter_color=None, background_color=None, shape=None,
                   orientation=None, notes=None, manual=None,
                   coord=None, width=None, height=None):
        self.target_region_id = target_region_id
        self.target_type = target_type
        self.letter = letter
        self.letter_color = letter_color
        self.background_color = background_color
        self.shape = shape
        self.orientation = orientation
        self.notes = notes
        self.coord = coord#((a['x'] + b['x']) / 2, (a['y'] + b['y']) / 2)