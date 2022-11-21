import logging

from flask import jsonify, request, url_for
from api import db
from api.models import Collection, Request
from api.v1 import bp


# from api.v1.helpers import Importer


#### COLLECTIONS ####
@bp.route("/v1/collections", methods=["GET"])
def get_collections():
    return jsonify(Collection.to_collection_dict(Collection.query))


@bp.route("/v1/collections/<int:id>", methods=["GET"])
def get_collection(collection_id: int):
    return jsonify(Collection.query.get_or_404(id).to_dict)


@bp.route("/v1/collections/", methods=["POST"])
def set_collection():
    data = request.get_json() or {}
    collection = data.get('collection') or {}
    requests = data.get('requests') or {}
    name = collection["name"]
    base_url = collection["base_url"]
    new_collection = Collection(name=name, base_url=base_url)
    db.session.add(new_collection)
    db.session.commit()
    response = jsonify(new_collection.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('v1.get_collection', id=new_collection.id)
    return response


#### REQUESTS ####
@bp.route("/v1/collections/requests", methods=["GET"])
def get_requests():
    return jsonify(Request.to_requests_dict(Request.query.all()))


@bp.route("/v1/collections/<int:id>/requests", methods=["GET"])
def get_request_by_collection_id(collection_id: int):
    return jsonify(Request.to_requests_dict(Request.query.get_or_404(collection_id)))


@bp.route("/v1/collections/<int:id>/requests", methods=["POST"])
def new_request(collection_id):
    data = request.get_json()
    request_name = data.get("name")
    request_collection = request.get("collection_id")
    try:
        result = Request(request_name, request_collection)
    except Exception as e:
        logging.log(e)
#
# @bp.route("/collections/<int:id>/run", ["POST"])
# def run_collection(collection_id: int):
#
