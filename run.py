import argparse
import json
import atexit

from ShimmerModel import ShimmerModel

from flask import Flask, request, send_file

app = Flask(__name__)
model = None # Model is initialized in __main__ block

class SimpleJsonEncoder(json.JSONEncoder):
    def default(self, o):
        return dict(o)

@app.route('/')
def index():
    """
    Serves the index page
    """
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def root(path):
    """
    Serves static files for the frontend.
    """
    return app.send_static_file(path)

@app.route('/view/targets')
def targets():
    """
    Serves the target view page.
    """
    return app.send_static_file('targets.html')

@app.route('/view/images')
def images():
    """
    Serves the image view page.
    """
    return app.send_static_file('images.html')

@app.route("/next", methods=['GET'])
def getNext():
    """
    Returns json of target data for next image
    """
    return json.dumps(model.get_next_image(), cls=SimpleJsonEncoder)

@app.route("/image/<int:idx>", methods=['GET'])
def getImage(idx):
    """
    Sends the image file for the image at index idx

    Arguments:
        idx: The index of the image to read
    """
    return send_file(open(model.img(idx).path, 'rb'), mimetype='image/jpg')

@app.route("/target/all", methods=['GET'])
def getAllTargets():
    return json.dumps(model.get_all_targets(), cls=SimpleJsonEncoder)

@app.route("/target/<int:id>", methods=['GET'])
def getTarget():
    return json.dumps(model.get_target(id), cls=SimpleJsonEncoder)

@app.route("/target/<int:id>", methods=['POST'])
def target(id):
    """
    Post new target data and update model with new targets
    """
    try:
        model.update_targets(id, json.loads(request.data.decode("utf-8"))["targets"])
    except IndexError:
        return "{\"status\":\"error\"}"
    return "{\"status\":\"ok\"}"

@app.route("/target/merge", methods=['POST'])
def mergeTargets():
    """
    Merge two or more target regions into one target
    """
    try:
        model.merge_targets(json.loads(request.data.decode("utf-8")))
    except IndexError:
        return "{\"status\":\"error\"}"
    return "{\"status\":\"ok\"}"

@app.route("/target/<int:id>", methods=['DELETE'])
def deleteTarget(id):
    """
    Delete the target with the given id
    """
    model.delete_target(id)
    return "{\"status\":\"ok\"}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog="You must specify either flight or directory.")
    parser.add_argument("-f", "--flight", type=int, help="Flight number")
    parser.add_argument("-d", "--directory", type=str, help="Directory to load images from")
    args = parser.parse_args()

    if bool(args.flight) == bool(args.directory):
        raise ValueError("You must specify either flight or directory.")

    if args.flight:
        from ARCImageQueue import ARCImageQueue
        queue = ARCImageQueue(args.flight)
    elif args.directory:
        from DirectoryImageQueue import DirectoryImageQueue
        queue = DirectoryImageQueue(args.directory)

    model = ShimmerModel(queue)

    def save_target_data():
        with open('targets.json', 'w') as file:
            json.dump(model.targets, file, indent=4)
    atexit.register(save_target_data)

    app.run(host='0.0.0.0')
