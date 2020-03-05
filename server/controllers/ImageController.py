import json

from flask import Blueprint, request, abort, send_file
from jinja2 import TemplateNotFound

from server.models.GlobalModel import get_model
from server.models.ShimmerTargetRegion import ShimmerTargetRegion
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
    except IndexError:
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
    except IndexError:
        abort(404)

@image_api.route("/<int:idx>/target", methods=['POST'])
@serialize
def postImageTarget(idx):
    response = json.loads(request.data.decode("utf-8"))
    target = response['target']
    target_region = response['target_region']

    return get_model().insert_target(idx, target, target_region)

@image_api.route("/<int:idx>/region/<int:tr_id>", methods=['GET'])
@serialize
def getTargetRegion(idx, tr_id):
    try:
        for target_region in get_model().img(idx).get_target_regions():
            if target_region.id == tr_id:
                return target_region
        abort(404)
    except KeyError:
        abort(404)

@image_api.route("/<int:idx>/region/<int:tr_id>", methods=['DELETE'])
def deleteTargetRegion(idx, tr_id):
    try:
        for target_region in get_model().img(idx).get_target_regions():
            if target_region.id == tr_id:
                target_region.target_region.delete_region()
                return '', 200
        abort(404)
    except KeyError:
        abort(404)


@image_api.route("/<int:idx>/targets-near", methods=['GET'])
@serialize
def getTargetsNear(idx):
    img = get_model().img(idx).image
    x = float(request.args.get("x"))
    y = float(request.args.get("y"))
    distance = float(request.args.get("distance", 50))
    coord = img.coord(x, y, to_wgs84=False)
    targets = get_model().get_targets_near(coord, distance)
    if targets is None:
        abort(406)
    return targets
