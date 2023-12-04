import pytest

from app.controllers import (
    BaseController,
    BeverageController,
    IngredientController,
    OrderController,
    SizeController,
)

from ..utils import get_random_choice, shuffle_list


def __order(size: dict, elements: list, client_data: dict):
    elements = [element.get("_id") for element in elements]
    size_id = size.get("_id")
    return {**client_data, "size_id": size_id, "elements": elements}


def __create_items(items: list, controller: BaseController):
    created_items = []
    for ingredient in items:
        created_item, _ = controller.create(ingredient)
        created_items.append(created_item)
    return created_items


def __create_sizes_and_elements(sizes: list, ingredients: list, beverages: list):
    created_ingredients = __create_items(ingredients, IngredientController)
    created_beverages = __create_items(beverages, BeverageController)
    created_sizes = __create_items(sizes, SizeController)
    created_elements = created_ingredients + created_beverages
    return (
        created_sizes if len(created_sizes) > 1 else created_sizes.pop(),
        created_elements,
    )


def test_create(app, size, ingredients, beverages, client_data):
    created_size, created_elements = __create_sizes_and_elements(
        [size], ingredients, beverages
    )
    order = __order(created_size, created_elements, client_data)
    created_order, error = OrderController.create(order)
    size_id = order.pop("size_id", None)
    element_ids = order.pop("elements", [])
    pytest.assume(error is None)
    for param, value in order.items():
        pytest.assume(param in created_order)
        pytest.assume(value == created_order[param])
        pytest.assume(created_order["_id"])
        pytest.assume(size_id == created_order["size"]["_id"])

        elements_in_detail = set(
            item["element"]["_id"] for item in created_order["detail"]
        )
        pytest.assume(not elements_in_detail.difference(element_ids))


def test_calculate_order_price(app, size, ingredients, beverages, client_data):
    created_size, created_elements = __create_sizes_and_elements(
        [size], ingredients, beverages
    )
    order = __order(created_size, created_elements, client_data)
    created_order, _ = OrderController.create(order)
    pytest.assume(
        created_order["total_price"]
        == round(
            created_size["price"]
            + sum(element["price"] for element in created_elements),
            2,
        )
    )


def test_update(app):
    update_order = {
        "client_name": "new name",
        "client_dni": "new dni",
        "client_address": "new address",
        "client_phone": "new phone",
    }
    updated_order, error = OrderController.update(1, update_order)
    pytest.assume(error is not None)
    pytest.assume(updated_order is None)


def test_get_by_id(app, size, ingredients, beverages, client_data):
    created_size, created_elements = __create_sizes_and_elements(
        [size], ingredients, beverages
    )
    order = __order(created_size, created_elements, client_data)
    created_order, _ = OrderController.create(order)
    order_from_db, error = OrderController.get_by_id(created_order["_id"])
    size_id = order.pop("size_id", None)
    element_ids = order.pop("elements", [])
    pytest.assume(error is None)
    for param, value in created_order.items():
        pytest.assume(order_from_db[param] == value)
        pytest.assume(size_id == created_order["size"]["_id"])

        elements_in_detail = set(
            item["element"]["_id"] for item in created_order["detail"]
        )
        pytest.assume(not elements_in_detail.difference(element_ids))


def test_get_all(app, sizes, ingredients, beverages, client_data):
    created_sizes, created_elements = __create_sizes_and_elements(
        sizes, ingredients, beverages
    )
    created_orders = []
    for _ in range(5):
        order = __order(
            get_random_choice(created_sizes),
            shuffle_list(created_elements)[:3],
            client_data,
        )
        created_order, _ = OrderController.create(order)
        created_orders.append(created_order)

    orders_from_db, error = OrderController.get_all()
    searchable_orders = {db_order["_id"]: db_order for db_order in orders_from_db}
    pytest.assume(error is None)
    for created_order in created_orders:
        current_id = created_order["_id"]
        assert current_id in searchable_orders
        for param, value in created_order.items():
            pytest.assume(searchable_orders[current_id][param] == value)
