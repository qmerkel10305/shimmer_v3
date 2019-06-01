import unittest
import json
import os

from flask import Flask

import server
from server.controllers.ImageController import image_api
from server.util.test.MockModel import with_mock_model
from server.util.test.MockImage import MockImage
from server.models.ShimmerImage import ShimmerImage

app = Flask(__name__)
app.register_blueprint(image_api, url_prefix='/image')

class TestImageController(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    @with_mock_model(images=[MockImage([])])
    def testGetNext(self):
        # Get first image
        image = self.app.get('/image/next')
        self.assertEquals(200, image._status_code)
        image = json.loads(image.data.decode("utf-8"))

        self.assertEquals(image["id"], 0)
        self.assertEquals(image["flight"], 1)
        self.assertEquals(image["targets"], [])

        # Out of images, should wrap back around
        image = self.app.get('/image/next')
        self.assertEquals(200, image._status_code)
        image = json.loads(image.data.decode("utf-8"))

        self.assertEquals(image["id"], 0)
        self.assertEquals(image["flight"], 1)
        self.assertEquals(image["targets"], [])

    @with_mock_model(images=[MockImage([])])
    def testGetImage(self):
        image = self.app.get('/image/0')
        self.assertEquals(200, image._status_code)
        image = json.loads(image.data.decode("utf-8"))

        self.assertEquals(image["id"], 0)
        self.assertEquals(image["flight"], 1)
        self.assertEquals(image["targets"], [])

    @with_mock_model(images=[MockImage([])])
    def testGetImageError(self):
        response = self.app.get('/image/1')
        self.assertEquals(404, response._status_code)

    @with_mock_model(images=[MockImage([])])
    def testGetImageJpg(self):
        image = self.app.get('/image/0/img.jpg')
        self.assertEquals(200, image._status_code)

        with open(os.path.abspath(os.path.join(server.util.test.__file__, os.pardir, "res", "img0.jpg")), 'rb') as f:
            raw_image = f.read()
            self.assertEquals(image.data, raw_image)