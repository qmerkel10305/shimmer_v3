from flask import Flask, request
import requests
import json
import pprint
import ARC

from flask import Flask
app = Flask(__name__)

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

@app.route('/<path:path>')
def root(path):
    return app.send_static_file(path)

# Response for GET business request
@app.route("/image", methods=['GET'])
def getImage():
    return "" + ARC.Target

# Register your name
@app.route("/target", methods=['POST'])
def target():
    print(json.dumps(json.loads(request.data), indent=4, sort_keys=True))
    return "thx"

# if '> python this.py' run Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0')
