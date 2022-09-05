import json

from flask import Blueprint, request, send_file, make_response

from server.models.GlobalModel import get_model
from server.util.decorators import serialize
from pathlib import Path

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

@target_api.route("/<int:target_id>/regions/<int:region_id>/thumb.jpg", methods=['GET'])
def getRegionThumbnail(target_id, region_id):
    response = make_response(send_file(get_model().get_region_from_target(target_id, region_id).thumbnail_path, mimetype='image/jpg'))
    response.cache_control.no_store = True
    return response

@target_api.route("/<int:id>/thumb.jpg", methods=['GET'])
def getTargetThumbnail(id):
    response = make_response(send_file(get_model().get_target(id).target.thumbnail, mimetype='image/jpg'))
    response.cache_control.no_store = True
    return response

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

@target_api.route("/database/image/<int:image_id>", methods=['GET'])
def getImageShimmerID(image_id):
    """
    Gets the id number of an image form the database number
    Used with target regions
    """
    return str(get_model().get_shimmer_image_id(image_id))

@target_api.route("/<int:target_id>/regions/<int:region_id>/update", methods=['POST'])
@serialize
def updateTargetThumbnail(target_id, region_id):
    get_model().get_region_from_target(target_id, region_id).update_target_thumbnail()


@target_api.route("/submit", methods=['GET'])
def submitTargets():
    targets = get_model().get_all_targets()
    client = get_model().client
    for t in targets:
        target_json = t.serialize_interop()
        print(target_json)
        odlc_id = client.post_odlc(target_json)
        print(t.target.thumbnail)
        client.put_odlc_image(odlc_id, Path(t.target.thumbnail).read_bytes())
    return str(odlc_id)
