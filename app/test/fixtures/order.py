import pytest

from ..fixtures.beverage import *
from ..utils.functions import get_random_sequence, get_random_string, shuffle_list


def client_data_mock() -> dict:
    return {
        "client_address": get_random_string(),
        "client_dni": get_random_sequence(),
        "client_name": get_random_string(),
        "client_phone": get_random_sequence(),
    }


@pytest.fixture
def order_uri():
    return "/order/"


@pytest.fixture
def client_data():
    return client_data_mock()


@pytest.fixture
def order(create_ingredients, create_size, create_beverages) -> dict:
    ingredients = [ingredient.get("_id") for ingredient in create_ingredients]
    beverages = [beverage.get("_id") for beverage in create_beverages]
    elements = ingredients + beverages
    size_id = create_size.json.get("_id")
    return {**client_data_mock(), "elements": elements, "size_id": size_id}


@pytest.fixture
def create_order(client, order_uri, order) -> dict:
    return client.post(order_uri, json=order)


@pytest.fixture
def create_orders(
    client, order_uri, create_ingredients, create_beverages, create_sizes
) -> list:
    ingredients = [ingredient.get("_id") for ingredient in create_ingredients]
    beverages = [beverage.get("_id") for beverage in create_beverages]
    elements = ingredients + beverages
    sizes = [size.get("_id") for size in create_sizes]
    orders = []
    for _ in range(10):
        new_order = client.post(
            order_uri,
            json={
                **client_data_mock(),
                "elements": shuffle_list(elements)[:5],
                "size_id": shuffle_list(sizes)[0],
            },
        )
        orders.append(new_order.json)
    return orders
