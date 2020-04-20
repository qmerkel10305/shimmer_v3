import json

from flask import Blueprint, request, abort, send_file
from jinja2 import TemplateNotFound

from server.models.GlobalModel import get_model
from server.models.ShimmerTarget import ShimmerTarget
from server.util.decorators import serialize

target_api = Blueprint('target_api', __name__)

@target_api.errorhandler(ValueError)
def handle_value_error(error):
    return str(error), 400

@target_api.errorhandler(KeyError)
def handle_key_error(error):
    return str(error), 404

@target_api.route("/", methods=['GET'])
@serialize
def getAllTargets():
    return get_model().get_all_targets()

@target_api.route("/<int:id>", methods=['GET'])
@serialize
def getTarget(id):
    return get_model().tgt(id)

@target_api.route("/<int:id>/thumb.jpg", methods=['GET'])
def getTargetThumbnail(id):
    return send_file(open(get_model().get_target(id).target.thumbnail, 'rb'), mimetype='image/jpg')

@target_api.route("/<int:target_id>", methods=['POST'])
@serialize
def postTarget(target_id):
    """
    Post new target data and update the model with new targets

    Currently unimplemented endpoint
    """
    return get_model().update_target(target_id, json.loads(request.data.decode("utf-8")))

@target_api.route("/merge/<int:target_id>", methods=['POST'])
@serialize
def mergeTargets(target_id):
    """
    Merge one or more targets into a target

    The merged targets will be deleted and their target regions will be
    attached to the base target region.
    """
    get_model().merge_targets(target_id, json.loads(request.data.decode("utf-8")))

@target_api.route("/<int:target_id>", methods=['DELETE'])
@serialize
def deleteTarget(target_id):
    """
    Delete the target with the given id
    """
    get_model().delete_target(target_id)

@target_api.route("/<int:target_id>/regions", methods=['GET'])
@serialize
def getTargetRegions(target_id):
    """
    Gets the target regions of a target id
    """
    return get_model().get_target_regions(target_id)

@target_api.route("/database/image/<int:image_id>")
def getImageShimmerID(image_id):
    """
    Gets the id number of an image form the database number
    Used with target regions
    """
    return get_model().get_shimmer_image_id(image_id)
