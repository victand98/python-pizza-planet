from ..controllers import IngredientController
from .blueprint import BaseBlueprint


class IngredientBlueprint(BaseBlueprint):
    def __init__(self) -> None:
        super().__init__("ingredient", __name__, IngredientController)


ingredient = IngredientBlueprint()
