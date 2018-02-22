import unittest

from ShimmerImage import ShimmerImage
from MockFlight import MockFlight
from MockImage import MockImage
from MockTarget import MockTarget

def create_mock_target():
    return MockTarget(1, None, 0, 'A', 'black', 'white', 'square', 0, '', {'x': 0, 'y': 0}, {'x': 1, 'y': 1})

def create_mock_target_and_dict(target_type=0, alphanumeric='A', alphanumeric_color='black',
                                shape_color='white', shape='square', alphanumeric_orientation=0,
                                notes='', a={'x': 0, 'y': 0}, b={'x': 1, 'y': 1},
                                width=1, height=1):
    dict_mock_target = {
        'target_type': target_type,
        'alphanumeric': alphanumeric,
        'alphanumeric_color': alphanumeric_color,
        'shape_color': shape_color,
        'shape': shape,
        'alphanumeric_orientation': alphanumeric_orientation,
        'notes': notes,
        'a': a,
        'b': b,
        'width': width,
        'height': height
    }
    mock_target = MockTarget(1, None, target_type=target_type, letter=alphanumeric,
                             letter_color=alphanumeric_color, background_color=shape_color,
                             shape=shape, orientation=alphanumeric_orientation,
                             notes=notes, width=width, height=height,
                             coord=((a['x'] + b['x'])/2, (a['y'] + b['y'])/2))
    return dict_mock_target, mock_target

class TestShimmerImage(unittest.TestCase):
    def setUp(self):
        ShimmerImage.next_id = 0
        self.image = ShimmerImage(MockImage([]), MockFlight())

    def testConstructor(self):
        self.assertEquals(0, self.image.id)
        self.assertEquals('image/0', self.image.image_url)
        self.assertEquals(0, len(self.image.targets))
        self.assertEquals(1, ShimmerImage.next_id)

    def testLoadTargets(self):
        mock_target = create_mock_target()
        self.image = ShimmerImage(MockImage([
                mock_target
        ]), MockFlight())

        self.assertEquals(1, len(self.image.targets))
        self.assertEquals(mock_target, self.image.targets[0].target_region)

    def testUpdateTargetsAdd(self):
        dict_mock_target, mock_target = create_mock_target_and_dict()
        self.image.update_targets([dict_mock_target])

        self.assertEquals(1, len(self.image.targets))
        self.assertEquals(mock_target.letter, self.image.targets[0].target_region.letter)

    def testUpdateTargetsDelete(self):
        mock_target = create_mock_target()
        self.image = ShimmerImage(MockImage([
                mock_target
        ]), MockFlight())

        self.image.update_targets([])

        self.assertEquals(0, len(self.image.targets))

    def testUpdateTargetsAddAndDelete(self):
        MockFlight.next_target_id = 1
        dict_mock_target1, mock_target1 = create_mock_target_and_dict(alphanumeric='A')
        dict_mock_target2, mock_target2 = create_mock_target_and_dict(alphanumeric='B')
        dict_mock_target3, mock_target3 = create_mock_target_and_dict(alphanumeric='C')
        self.image.update_targets([dict_mock_target1, dict_mock_target2])

        # Set the target_id of this target so that the ShimmerImage recognizes it
        # as a target it has already seen
        dict_mock_target1['target_id'] = 1

        self.assertEquals(2, len(self.image.targets))
        self.assertEquals(mock_target1.letter, self.image.targets[0].target_region.letter)
        self.assertEquals(mock_target2.letter, self.image.targets[1].target_region.letter)

        self.image.update_targets([dict_mock_target1, dict_mock_target3])

        self.assertEquals(2, len(self.image.targets))
        self.assertEquals(mock_target1.letter, self.image.targets[0].target_region.letter)
        self.assertEquals(mock_target3.letter, self.image.targets[1].target_region.letter)

    def tearDown(self):
        pass