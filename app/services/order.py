from ..controllers import OrderController
from .blueprint import BaseBlueprint


class OrderBlueprint(BaseBlueprint):
    def __init__(self) -> None:
        super().__init__("order", __name__, OrderController)


order = OrderBlueprint()
