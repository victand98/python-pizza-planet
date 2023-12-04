from flask import Blueprint, jsonify

from ..common import GET, NOT_FOUND, OK
from ..controllers import ReportController

report = Blueprint("report", __name__)


@report.route("/", methods=GET)
def generate_report():
    report = ReportController.generate_report()
    status_code = OK if report else NOT_FOUND
    return jsonify(report), status_code
