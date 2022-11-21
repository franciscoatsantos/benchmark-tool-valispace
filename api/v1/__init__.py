from flask import Blueprint

bp = Blueprint('v1', __name__)

from api.v1 import collections, monitors
