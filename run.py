import argparse
import json

from ShimmerQueue import ShimmerQueue

from flask import Flask, request
app = Flask(__name__)

# Queue of images that are ready to
# have their target's classified

parser = argparse.ArgumentParser(epilog="You must specify either flight or directory.")
parser.add_argument("-f", "--flight", type=int, help="Flight number")
parser.add_argument("-d", "--directory", type=str, help="Directory to load images from")
args = parser.parse_args()

if bool(args.flight) == bool(args.directory): # effectively an XOR
    raise ValueError("You must specify either flight or directory.")

if args.flight:
    from ARCImageQueue import ARCImageQueue
    queue = ARCImageQueue(args.flight)
elif args.directory:
    from DirectoryImageQueue import DirectoryImageQueue
    queue = DirectoryImageQueue(args.directory)

images = ShimmerQueue(queue)

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
    return json.dumps(images.get_next_image())

@app.route("/image/<path:path>", methods=['GET'])
def getImage(path):
    with open(path, 'rb') as f:
        return f.read()

# Serves static files for the frontend program
@app.route('/<path:path>')
def root(path):
    return app.send_static_file(path)

# Post target data, path should be image id in the flight
@app.route("/target/<int:id>", methods=['POST'])
def target(id):
    try:
        images.targets[id] = json.loads(request.data.decode("utf-8"))
    except IndexError:
        return "{\"status\":\"error\"}"
    return "{\"status\":\"ok\"}"

# if '> python run.py' run Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0')
