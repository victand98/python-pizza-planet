import pytest

from app.common import BAD_REQUEST, CREATED, OK

from ..utils import get_random_string


def test_create_order_service(create_order):
    order = create_order.json
    pytest.assume(create_order.status.startswith(str(CREATED)))
    pytest.assume(order["_id"])
    pytest.assume(order["size"])
    pytest.assume(order["detail"])
    pytest.assume(order["date"])
    pytest.assume(order["total_price"])
    pytest.assume(order["client_name"])
    pytest.assume(order["client_address"])
    pytest.assume(order["client_dni"])
    pytest.assume(order["client_phone"])


def test_update_order_service(client, create_order, order_uri):
    current_order = create_order.json
    update_data = {
        **current_order,
        "client_name": get_random_string(),
        "client_address": get_random_string(),
        "client_dni": get_random_string(),
        "client_phone": get_random_string(),
    }
    response = client.put(f'{order_uri}{current_order["_id"]}', json=update_data)
    pytest.assume(response.status.startswith(str(BAD_REQUEST)))


def test_get_order_by_id_service(client, create_order, order_uri):
    current_order = create_order.json
    response = client.get(f'{order_uri}{current_order["_id"]}')
    pytest.assume(response.status.startswith(str(OK)))
    returned_order = response.json
    for param, value in current_order.items():
        pytest.assume(returned_order[param] == value)


def test_get_orders_service(client, create_orders, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith(str(OK)))
    returned_orders = {order["_id"]: order for order in response.json}
    for order in create_orders:
        pytest.assume(order["_id"] in returned_orders)
