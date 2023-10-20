from ..repositories.managers import (OrderManager)
from .base import BaseController
from ..creators import DefaultOrderCreator


class OrderController(BaseController):
    manager = OrderManager
    order_creator = DefaultOrderCreator()

    def __init__(self, order_creator=None):
        if order_creator:
            self.order_creator = order_creator

    def create(self, order: dict):
        return self.order_creator.create(order)
