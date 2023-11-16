from ..controllers import BeverageController
from .blueprint import BaseBlueprint


class BeverageBlueprint(BaseBlueprint):
    def __init__(self) -> None:
        super().__init__("beverage", __name__, BeverageController)


beverage = BeverageBlueprint()
