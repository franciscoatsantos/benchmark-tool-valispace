from flask import jsonify, request
from api.models import Collection, Request
from api.v1 import bp


@bp.route("/collections", ["GET"])
def get_collections():
    return jsonify(Collection.query.all().to_dict())


@bp.route("/collections/<int:id>", ["GET"])
def get_collection(collection_id: int):
    return jsonify(Collection.query.get_or_404(id).to_dict())


@bp.route("/collections/requests", ["GET"])
def get_requests():
    return jsonify(Request.query.all().to_dict())


@bp.route("/collections/<int:id>/requests", ["GET"])
def get_request_by_collection_id(collection_id: int):
    return jsonify(Request.query.get_or_404(collection_id).to_dict())


@bp.route("/collections/", ["POST"])
def set_collection():
    data = request.get_json() or {}

