import unittest
import json

from server.models.ShimmerImage import ShimmerImage

from server.util.test.MockFlight import MockFlight
from server.util.test.MockImage import MockImage

from generate import create_mock_target, create_mock_target_and_dict, create_mock_target_region_and_dict

class TestShimmerImage(unittest.TestCase):
    def setUp(self):
        self.image = ShimmerImage(0, MockImage([]), MockFlight())

    def testConstructor(self):
        self.assertEquals(0, self.image.id)
        self.assertEquals(0, len(self.image.targets))

    def testSerialize(self):
        image = self.image.serialize()
        self.assertEquals(image["id"], 0)
        self.assertEquals(image["flight"], 1)
        self.assertEquals(image["targets"], [])

    def testLoadTargets(self):
        _, mock_target = create_mock_target_region_and_dict()
        self.image = ShimmerImage(0, MockImage([
            mock_target
        ]), MockFlight())

        self.assertEquals(1, len(self.image.targets))
        self.assertEquals(mock_target, self.image.targets[0].target_region)

    def tearDown(self):
        pass