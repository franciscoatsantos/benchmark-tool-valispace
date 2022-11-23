import logging

import jsonref
from flask import jsonify, request
from api import db
from api.models import Collection, Request
from api.v1 import bp
from api.v1.helpers import Importer


#### COLLECTIONS ####
@bp.route("/v1/collections", methods=["GET"])
def get_collections():
    return jsonify(Collection.to_collection_dict(Collection.query.all()))


@bp.route("/v1/collections/<int:id>", methods=["GET"])
def get_collection(collection_id: int):
    return jsonify(Collection.query.get_or_404(id).to_dict)


@bp.route("/v1/collections/", methods=["POST"])
def set_collection():
    data = request.get_json()
    new_data = Importer.import_collection(data=data, filters=["get"])
    collection = Collection()
    collection.from_dict(new_data["collection"])
    db.session.add(collection)
    db.session.commit()
    for new_request in new_data["requests"]:
        new_request["collection_id"] = collection.id
        request_model = Request()
        request_model.from_dict(new_request)
        db.session.add(request_model)
    db.session.commit()
    response = jsonify(collection.to_dict())
    return response


#### REQUESTS ####
@bp.route("/v1/collections/requests", methods=["GET"])
def get_requests():
    return jsonify(Request.to_requests_dict(Request.query.all()))


@bp.route("/v1/collections/<int:id>/requests", methods=["GET"])
def get_request_by_collection_id(collection_id: int):
    return jsonify(Request.to_requests_dict(Request.query.get_or_404(collection_id)))


@bp.route("/v1/collections/<int:id>/requests", methods=["POST"])
def set_request(collection_id):
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
