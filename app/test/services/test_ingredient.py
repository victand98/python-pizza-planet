import pytest

from app.common import CREATED, OK

from ..utils import get_random_price, get_random_string


def test_create_ingredient_service(create_ingredient):
    ingredient = create_ingredient.json
    pytest.assume(create_ingredient.status.startswith(str(CREATED)))
    pytest.assume(ingredient["_id"])
    pytest.assume(ingredient["name"])
    pytest.assume(ingredient["price"])


def test_update_ingredient_service(client, create_ingredient, ingredient_uri):
    current_ingredient = create_ingredient.json
    update_data = {
        **current_ingredient,
        "name": get_random_string(),
        "price": get_random_price(1, 5),
    }
    response = client.put(
        f'{ingredient_uri}{current_ingredient["_id"]}', json=update_data
    )
    pytest.assume(response.status.startswith(str(OK)))
    updated_ingredient = response.json
    for param, value in update_data.items():
        pytest.assume(updated_ingredient[param] == value)


def test_get_ingredient_by_id_service(client, create_ingredient, ingredient_uri):
    current_ingredient = create_ingredient.json
    response = client.get(f'{ingredient_uri}{current_ingredient["_id"]}')
    pytest.assume(response.status.startswith(str(OK)))
    returned_ingredient = response.json
    for param, value in current_ingredient.items():
        pytest.assume(returned_ingredient[param] == value)


def test_get_ingredients_service(client, create_ingredients, ingredient_uri):
    response = client.get(ingredient_uri)
    pytest.assume(response.status.startswith(str(OK)))
    returned_ingredients = {
        ingredient["_id"]: ingredient for ingredient in response.json
    }
    for ingredient in create_ingredients:
        pytest.assume(ingredient["_id"] in returned_ingredients)
