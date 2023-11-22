from ..controllers import SizeController
from .blueprint import BaseBlueprint


class SizeBlueprint(BaseBlueprint):
    def __init__(self) -> None:
        super().__init__("size", __name__, SizeController)


size = SizeBlueprint()
