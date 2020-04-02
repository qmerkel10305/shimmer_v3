import unittest
import json

from server.models.ShimmerTargetRegion import ShimmerTargetRegion

from generate import create_mock_target_region_and_dict, create_mock_incorrect_region

class TestShimmerImage(unittest.TestCase):
    def setUp(self):
        _, target_region = create_mock_target_region_and_dict()
        self.target_region = ShimmerTargetRegion(target_region)

    def testConstructor(self):
        self.assertEquals(1, self.target_region.id)
        # TODO Test other attributes

    def testSerialize(self):
        target_region = self.target_region.serialize()
        self.assertEquals(target_region["id"], 1)
        # TODO Test other attributes

    def testCheck_Corners(self):
        self.assertEquals(False, self.target_region.check_corners())
        test = create_mock_incorrect_region()
        test_region = ShimmerTargetRegion(test)
        self.assertEquals(True, test_region.check_corners())

