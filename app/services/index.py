from flask import Blueprint, jsonify

from ..common import GET
from ..controllers import IndexController

index = Blueprint("index", __name__)


@index.route("/", methods=GET)
def get_index():
    is_database_up, error = IndexController.test_connection()
    return jsonify(
        {
            "version": "0.0.2",
            "status": "up" if is_database_up else "down",
            "error": error,
        }
    )
