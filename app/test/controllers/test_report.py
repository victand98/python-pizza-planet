import pytest

from app.controllers import ReportController

from ..fixtures.report import *


def test_generate_report(app, create_orders):
    report_controller = ReportController()
    report = report_controller.generate_report()
    pytest.assume(report["the_most_requested_ingredient"])
    pytest.assume(report["the_most_requested_beverage"])
    pytest.assume(report["month_with_more_revenue"])
    pytest.assume(report["top_customers"])
