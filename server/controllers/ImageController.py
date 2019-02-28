import json

from flask import Blueprint, request, abort, send_file
from jinja2 import TemplateNotFound

from server.models.GlobalModel import get_model
from server.util.decorators import serialize

image_api = Blueprint('image_api', __name__)

@image_api.route("/next", methods=['GET'])
@serialize
def getNext():
    """
    Returns json of target data for next image
    """
    return get_model().get_next_image()

@image_api.route("/<int:idx>", methods=['GET'])
@serialize
def getImage(idx):
    """
    Send the data about an image at index idx

    Arguments:
        idx: The index of the image to read
    """
    try:
        return get_model().img(idx)
    except KeyError:
        abort(404)

@image_api.route("/<int:idx>/img.jpg", methods=['GET'])
def getImageJpg(idx):
    """
    Sends the image file for the image at index idx

    Arguments:
        idx: The index of the image to read
    """
    try:
        return send_file(open(get_model().img(idx).path, 'rb'), mimetype='image/jpg')
    except KeyError:
        abort(404)

@image_api.route("/<int:idx>/target", methods=['POST'])
@serialize
def postImageTarget(idx):
    response = json.loads(request.data.decode("utf-8"))
    target = response['target']
    target_region = response['target_region']

    return get_model().insert_target(idx, target, target_region)