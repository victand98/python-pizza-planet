from app.common.http_methods import GET
from flask import Blueprint, jsonify

from ..controllers import ReportController

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def generate_report():
    report_controller = ReportController()
    report = report_controller.generate_report()
    status_code = 200 if report else 404
    return jsonify(report), status_code
