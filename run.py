from flask import Flask, request
import requests
import json
import pprint
# import ARC

from flask import Flask
app = Flask(__name__)

# Queue of images that are ready to
# have their target's classified

targets = dict()

targets["0"] = """{
    "id": 0,
    "targets": [
        {
            "a": {
                "x": 1985.6888888888889,
                "y": 1084.8264462809918
            },
            "b": {
                "x": 2264.5777777777776,
                "y": 1314.3801652892562
            },
            "height": 229.55371900826435,
            "width": 278.8888888888887
        }
    ]
}"""

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
    return targets["0"]

@app.route("/image/<path:path>", methods=['GET'])
def getImage(path):
    return targets[path]

# Serves static files for the frontend program
@app.route('/<path:path>')
def root(path):
    return app.send_static_file(path)

# Post target data, path should be image id in the flight
@app.route("/target/<path:path>", methods=['POST'])
def target(path):
    targets[path] = request.data;
    # print(json.dumps(json.loads(request.data), indent=4, sort_keys=True))
    return "{\"status\":\"ok\"}"

# if '> python run.py' run Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0')
