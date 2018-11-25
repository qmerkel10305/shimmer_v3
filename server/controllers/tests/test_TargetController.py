import unittest
import json

from flask import Flask

from server.controllers.TargetController import target_api
from server.util.test.MockModel import with_mock_model
from server.util.test.MockTarget import MockTarget
from server.util.test.MockImage import MockImage

app = Flask(__name__)
app.register_blueprint(target_api, url_prefix='/target')

def create_mock_target():
    return MockTarget(1, image=MockImage([]), target_type=0, letter='A', letter_color='black',
                    shape_color='white', shape='square', orientation=0, notes='', manual=True)

class TestTargetController(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    @with_mock_model(targets=[create_mock_target()])
    def testGetAll(self):
        targets = self.app.get('/target/')
        self.assertEquals(200, targets._status_code)
        targets = json.loads(targets.data.decode("utf-8"))

        self.assertEquals(1, len(targets))

        target = targets[0]
        self.assertEquals(1, target["id"])