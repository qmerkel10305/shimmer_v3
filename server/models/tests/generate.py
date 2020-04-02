from server.util.test.MockFlight import MockFlight
from server.util.test.MockImage import MockImage
from server.util.test.MockTarget import MockTarget
from server.util.test.MockTargetRegion import MockTargetRegion

def create_mock_target():
    return MockTarget(1, image=None, target_type=0, letter='A', letter_color='black',
                    shape_color='white', shape='square', orientation=0, notes='', manual=True)

def create_mock_target_and_dict(target_type=0, alphanumeric='A', alphanumeric_color='black',
                                shape_color='white', shape='square', alphanumeric_orientation=0,
                                notes=''):
    dict_mock_target = {
        'target_type': target_type,
        'letter': alphanumeric,
        'letter_color': alphanumeric_color,
        'shape_color': shape_color,
        'shape': shape,
        'orientation': alphanumeric_orientation,
        'notes': notes
    }
    mock_target = MockTarget(1, None, target_type=target_type, letter=alphanumeric,
                             letter_color=alphanumeric_color, shape_color=shape_color,
                             shape=shape, orientation=alphanumeric_orientation, notes=notes)
    return dict_mock_target, mock_target

def create_mock_target_region_and_dict(a={'x': 0, 'y': 0}, b={'x': 1, 'y': 1}):
    dict_mock_target = {
        'id': 1,
        'target_id': 1,
        'image_id': 1,
        'a': a,
        'b': b
    }
    mock_target = MockTargetRegion(1, target=create_mock_target(),image=None, flight=MockFlight(mock_directory=True),
                                   coord1=(a['x'], a['y']), coord2=(b['x'], b['y']))
    mock_target.image = MockImage([mock_target])
    return dict_mock_target, mock_target

def create_mock_incorrect_region(a={'x': 0, 'y': 1}, b={'x': 1, 'y': 0}):
    mock_target = MockTargetRegion(1, target=create_mock_target(),image=None, flight=MockFlight(mock_directory=True),
                               coord1=(a['x'], a['y']), coord2=(b['x'], b['y']))
    mock_target.image = MockImage([mock_target])
    return mock_target

