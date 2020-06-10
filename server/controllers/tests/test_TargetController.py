import os
import unittest
import json

from flask import Flask

import server
from server.models.ShimmerTarget import ShimmerTarget
from server.controllers.TargetController import target_api
from server.util.test.MockModel import with_mock_model
from server.util.test.MockTarget import MockTarget
from server.util.test.MockImage import MockImage

import server.models.GlobalModel as GlobalModel

app = Flask(__name__)
app.register_blueprint(target_api, url_prefix='/target')

def create_mock_target(target_id=1):
    return MockTarget(target_id, image=MockImage([]), target_type=0, letter='A', letter_color='black',
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
        self.assertEquals(0, target["target_type"])
        self.assertEquals("A", target["letter"])
        self.assertEquals("black", target["letter_color"])
        self.assertEquals("square", target["shape"])
        self.assertEquals("white", target["shape_color"])
        self.assertEquals(0, target["orientation"])
        self.assertEquals("", target["notes"])
        self.assertEquals(True, target["manual"])

    @with_mock_model(targets=[create_mock_target()])
    def testGet(self):
        target = self.app.get('/target/1')
        self.assertEquals(200, target._status_code)
        target = json.loads(target.data.decode("utf-8"))

        self.assertEquals(1, target["id"])
        self.assertEquals(0, target["target_type"])
        self.assertEquals("A", target["letter"])
        self.assertEquals("black", target["letter_color"])
        self.assertEquals("square", target["shape"])
        self.assertEquals("white", target["shape_color"])
        self.assertEquals(0, target["orientation"])
        self.assertEquals("", target["notes"])
        self.assertEquals(True, target["manual"])

    @with_mock_model(targets=[create_mock_target()])
    def testThumbnailGet(self):
        target = self.app.get('/target/1/thumb.jpg')
        self.assertEquals(200, target._status_code)
        with open(os.path.abspath(os.path.join(server.util.test.__file__, os.pardir, "res", "target01.jpg")), 'rb') as f:
            raw_image = f.read()
            self.assertEquals(target.data, raw_image)

    @with_mock_model(targets=[create_mock_target()])
    def testTargetPostError(self):
        new_target =  ShimmerTarget(MockTarget(2, image=MockImage([]),
            target_type=0, letter='A', letter_color='black', shape_color='white',
            shape='square', orientation=0, notes='', manual=True))

        target = self.app.post('/target/1', json=new_target.serialize())
        self.assertEquals(400, target._status_code)

        new_target =  ShimmerTarget(MockTarget(1, image=MockImage([]),
            target_type=0, letter='A', letter_color='black', shape_color='white',
            shape='square', orientation=0, notes='', manual=False))

        target = self.app.post('/target/1', json=new_target.serialize())
        self.assertEquals(400, target._status_code)

    @with_mock_model(targets=[create_mock_target()])
    def testTargetPost(self):
        new_target = MockTarget(1, image=MockImage([]), target_type=0,
            letter='B', letter_color='white', shape_color='black',
            shape='circle', orientation=359, notes='Test', manual=True)

        target = self.app.post('/target/1', json=ShimmerTarget(new_target).serialize())
        self.assertEquals(200, target._status_code)
        target = json.loads(target.data.decode("utf-8"))

        self.assertEquals(new_target.target_id, target["id"])
        self.assertEquals(new_target.target_type, target["target_type"])
        self.assertEquals(new_target.letter, target["letter"])
        self.assertEquals(new_target.letter_color, target["letter_color"])
        self.assertEquals(new_target.shape, target["shape"])
        self.assertEquals(new_target.background_color, target["shape_color"])
        self.assertEquals(new_target.orientation, target["orientation"])
        self.assertEquals(new_target.notes, target["notes"])
        self.assertEquals(new_target.manual, target["manual"])

    @with_mock_model(targets=[create_mock_target()])
    def testTargetDelete(self):
        target = self.app.get('/target/1')
        self.assertEquals(200, target._status_code)

        self.app.delete('/target/1')

        target = self.app.get('/target/1')
        print(GlobalModel.model.queue.flight)
        self.assertEquals(404, target._status_code)


    @with_mock_model(targets=[create_mock_target(), create_mock_target(target_id=2)])
    def testTargetMerge(self):
        targets = json.loads(self.app.get('/target/').data.decode("utf-8"))
        self.assertEquals(2, len(targets))

        response = self.app.post('/target/merge/1', json=[2])
        self.assertEquals(200, response._status_code)

        targets = json.loads(self.app.get('/target/').data.decode("utf-8"))
        self.assertEquals(1, len(targets))
