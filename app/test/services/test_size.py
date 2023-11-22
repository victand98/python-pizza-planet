import pytest

from app.common import CREATED, OK

from ..utils import get_random_price, get_random_string


def test_create_size_service(create_size):
    size = create_size.json
    pytest.assume(create_size.status.startswith(str(CREATED)))
    pytest.assume(size["_id"])
    pytest.assume(size["name"])
    pytest.assume(size["price"])


def test_update_size_service(client, create_size, size_uri):
    current_size = create_size.json
    update_data = {
        **current_size,
        "name": get_random_string(),
        "price": get_random_price(1, 5),
    }
    response = client.put(f'{size_uri}{current_size["_id"]}', json=update_data)
    pytest.assume(response.status.startswith(str(OK)))
    updated_size = response.json
    for param, value in update_data.items():
        pytest.assume(updated_size[param] == value)


def test_get_size_by_id_service(client, create_size, size_uri):
    current_size = create_size.json
    response = client.get(f'{size_uri}{current_size["_id"]}')
    pytest.assume(response.status.startswith(str(OK)))
    returned_size = response.json
    for param, value in current_size.items():
        pytest.assume(returned_size[param] == value)


def test_get_all_sizes_service(client, create_sizes, size_uri):
    response = client.get(size_uri)
    pytest.assume(response.status.startswith(str(OK)))
    returned_sizes = {size["_id"]: size for size in response.json}
    for size in create_sizes:
        pytest.assume(size["_id"] in returned_sizes)
