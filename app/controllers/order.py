from sqlalchemy.exc import SQLAlchemyError

from ..common import check_required_keys
from ..repositories import ElementManager, OrderManager, SizeManager
from .base import BaseController


class OrderController(BaseController):
    manager = OrderManager
    __required_info = (
        "client_name",
        "client_dni",
        "client_address",
        "client_phone",
        "size_id",
    )

    @staticmethod
    def calculate_order_price(size_price: float, elements: list):
        price = size_price
        price += sum(element.price for element in elements)

        return round(price, 2)

    @classmethod
    def create(cls, order: dict):
        current_order = order.copy()
        if not check_required_keys(cls.__required_info, current_order):
            return "Invalid order payload", None

        try:
            size_id = current_order.get("size_id")
            size = SizeManager.get_by_id(size_id)

            if not size:
                return "Invalid size for Order", None

            element_ids = current_order.pop("elements", [])
            elements = ElementManager.get_by_id_list(element_ids)

            price = cls.calculate_order_price(size.get("price"), elements)
            order_with_price = {**current_order, "total_price": price}
            return cls.manager.create(order_with_price, elements), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
