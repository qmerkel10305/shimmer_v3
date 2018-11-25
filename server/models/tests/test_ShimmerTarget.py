import unittest

from server.models.ShimmerTarget import ShimmerTarget

from generate import create_mock_target

class TestShimmerImage(unittest.TestCase):
    def setUp(self):
        self.target = ShimmerTarget(create_mock_target())

    def testConstructor(self):
        self.assertEquals(1, self.target.id)
        # TODO Test other attributes

    def testSerialize(self):
        target = self.target.serialize()
        self.assertEquals(target["id"], 1)
        # TODO Test other attributes
