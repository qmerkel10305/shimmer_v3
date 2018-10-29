import argparse
import json

from flask import Flask, request, send_file

from server.ShimmerModel import ShimmerModel
from server.util.decorators import serialize

app = Flask(__name__)
model = None # Model is initialized in __main__ block

@app.route('/')
def index():
    """
    Serves the index page
    """
    return app.send_static_file('index.html')

@app.route('/targets')
def targets():
    """
    Serves the target view page.
    This actually serves the index page, but Angular renders the page this way.
    """
    return app.send_static_file('index.html')

@app.route('/images')
def images():
    """
    Serves the image view page.
    This actually serves the index page, but Angular renders the page this way.
    """
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def root(path):
    """
    Serves static files for the frontend.
    """
    return app.send_static_file(path)

@app.route("/next", methods=['GET'])
@serialize
def getNext():
    """
    Returns json of target data for next image
    """
    return model.get_next_image()

@app.route("/image/<int:idx>", methods=['GET'])
@serialize
def getImage(idx):
    """
    Send the data about an image at index idx

    Arguments:
        idx: The index of the image to read
    """
    return model.img(idx)

@app.route("/image/<int:idx>/img.jpg", methods=['GET'])
def getImageJpg(idx):
    """
    Sends the image file for the image at index idx

    Arguments:
        idx: The index of the image to read
    """
    return send_file(open(model.img(idx).path, 'rb'), mimetype='image/jpg')

@app.route("/target/all", methods=['GET'])
@serialize
def getAllTargets():
    return model.get_all_targets()

@app.route("/target/<int:id>", methods=['GET'])
@serialize
def getTarget():
    return model.get_target(id)

@app.route("/target/<int:id>/thumb.jpg", methods=['GET'])
def getTargetThumbnail(id):
    return send_file(open(model.get_target(id).target_region.target.thumbnail, 'rb'), mimetype='image/jpg')

@app.route("/target/<int:id>", methods=['POST'])
@serialize
def target(id):
    """
    Post new target data and update model with new targets
    """
    model.update_targets(id, json.loads(request.data.decode("utf-8"))["targets"])

@app.route("/target/merge", methods=['POST'])
@serialize
def mergeTargets():
    """
    Merge two or more target regions into one target
    """
    model.merge_targets(json.loads(request.data.decode("utf-8")))

@app.route("/target/<int:id>", methods=['DELETE'])
@serialize
def deleteTarget(id):
    """
    Delete the target with the given id
    """
    model.delete_target(id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog="You must specify either flight or directory.")
    parser.add_argument("-f", "--flight", type=int, help="Flight number")
    parser.add_argument("-d", "--directory", type=str, help="Directory to load images from")
    args = parser.parse_args()

    if bool(args.flight) == bool(args.directory):
        raise ValueError("You must specify either flight or directory.")

    if args.flight:
        from server.ARCImageQueue import ARCImageQueue
        queue = ARCImageQueue(args.flight)
    elif args.directory:
        from server.DirectoryImageQueue import DirectoryImageQueue
        queue = DirectoryImageQueue(args.directory)

    model = ShimmerModel(queue)

    app.run(host='0.0.0.0')
