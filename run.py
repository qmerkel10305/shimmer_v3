from flask import Flask, request
import argparse
import requests
import json
import pprint
from DirectoryImageQueue import DirectoryImageQueue

from flask import Flask
app = Flask(__name__)

# Queue of images that are ready to
# have their target's classified

next_id = 0

targets = dict()

images = DirectoryImageQueue("img")

image_list = None

def image_iterator():
    """
    A generator used to replay the old images after the image
    queue has been exhausted.
    """
    for _, img in targets.items():
        yield img

# Sort image data in some list / tree
# Need to import ARC library to add targets to tables
#   --> Get targets for images so frontend can see previously inserted targets
# Flight # will be set backend but in the future maybe frontend can select that

class Target:
    def __init__(self):
        self.image = ''
        self.x = 0
        self.y = 0

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Returns json of target data for next image and url for the next image
@app.route("/next", methods=['GET'])
def getNext():
    global next_id
    next_img = images.get_next_image()
    if not next_img:
        return json.dumps(getReplayImage())
    targets[next_id] = {
        "id": next_id,
        "image": next_img,
        "targets": []
    }
    next_id += 1
    return json.dumps(targets[next_id - 1])

def getReplayImage():
    """
    Replays images in a loop
    """
    global image_list
    try:
        next_data = next(image_list)
    except (StopIteration, TypeError):
        # Restart the image generator
        image_list = image_iterator()
        try:
            next_data = next(image_list)
        except StopIteration:
            # There were no images in the queue at any point,
            # so there is nothing to show.
            return { "error": "No images" }
    return next_data

@app.route("/image/<int:id>", methods=['GET'])
def getImageData(id):
    try:
        return json.dumps(targets[id])
    except KeyError:
        return json.dumps({ "error": "No such id " + id })

@app.route("/image/raw/<path:path>", methods=['GET'])
def getRawImage(path):
    with open(path, 'rb') as f:
        return f.read()

# Serves static files for the frontend program
@app.route('/<path:path>')
def root(path):
    return app.send_static_file(path)

# Post target data, path should be image id in the flight
@app.route("/target/<path:path>", methods=['POST'])
def target(path):
    targets[path] = json.loads(request.data.decode("utf-8"))
    return "{\"status\":\"ok\"}"

# if '> python run.py' run Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0')
