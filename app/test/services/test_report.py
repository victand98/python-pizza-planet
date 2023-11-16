import pytest

from app.common import OK

from ..fixtures.report import *


def test_generate_report_service(client, report_uri, create_orders):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith(str(OK)))
    report = response.json
    pytest.assume(report["the_most_requested_ingredient"])
    pytest.assume(report["month_with_more_revenue"])
    pytest.assume(report["top_customers"])
