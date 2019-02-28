import json

from flask import Blueprint, request, abort, send_file
from jinja2 import TemplateNotFound

from server.models.GlobalModel import get_model
from server.models.ShimmerTarget import ShimmerTarget
from server.util.decorators import serialize

target_api = Blueprint('target_api', __name__)

@target_api.route("/", methods=['GET'])
@serialize
def getAllTargets():
    return get_model().get_all_targets()

@target_api.route("/<int:id>", methods=['GET'])
@serialize
def getTarget(id):
    for target in get_model().get_all_targets():
        if target.id == id:
            return target
    abort(404)

@target_api.route("/<int:id>/thumb.jpg", methods=['GET'])
def getTargetThumbnail(id):
    return send_file(open(get_model().get_target(id).target_region.target.thumbnail, 'rb'), mimetype='image/jpg')

@target_api.route("/<int:id>", methods=['POST'])
@serialize
def target(id):
    """
    Post new target data and update get_model() with new targets
    """
    get_model().update_targets(id, json.loads(request.data.decode("utf-8"))["targets"])

@target_api.route("/merge", methods=['POST'])
@serialize
def mergeTargets():
    """
    Merge two or more target regions into one target
    """
    get_model().merge_targets(json.loads(request.data.decode("utf-8")))

@target_api.route("/<int:id>", methods=['DELETE'])
@serialize
def deleteTarget(id):
    """
    Delete the target with the given id
    """
    get_model().delete_target(id)
