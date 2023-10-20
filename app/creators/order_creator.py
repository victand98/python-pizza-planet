from abc import ABC, abstractmethod
from sqlalchemy.exc import SQLAlchemyError

from ..common.utils import check_required_keys
from ..repositories.managers import (
    BeverageManager, IngredientManager, SizeManager, OrderManager)


class OrderCreator(ABC):
    @abstractmethod
    def get_required_info(self):
        pass

    @abstractmethod
    def get_size(self, size_id):
        pass

    @abstractmethod
    def get_ingredients(self, ingredient_ids):
        pass

    @abstractmethod
    def get_beverages(self, beverage_ids):
        pass

    @abstractmethod
    def calculate_order_price(self, size_price, ingredients, beverages):
        pass

    @abstractmethod
    def create_order(self, order_with_price, ingredients, beverages):
        pass

    def create(self, order: dict):
        current_order = order.copy()
        if not check_required_keys(self.get_required_info(), current_order):
            return 'Invalid order payload', None

        size_id = current_order.get('size_id')
        size = self.get_size(size_id)

        if not size:
            return 'Invalid size for Order', None

        ingredient_ids = current_order.pop('ingredients', [])
        beverage_ids = current_order.pop('beverages', [])

        try:
            ingredients = self.get_ingredients(ingredient_ids)
            beverages = self.get_beverages(beverage_ids)
            price = self.calculate_order_price(
                size.get('price'), ingredients, beverages)
            order_with_price = {**current_order, 'total_price': price}
            return self.create_order(order_with_price, ingredients, beverages), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)


class DefaultOrderCreator(OrderCreator):
    manager = OrderManager

    def get_required_info(self):
        return ('client_name', 'client_dni', 'client_address', 'client_phone', 'size_id')

    def get_size(self, size_id):
        return SizeManager.get_by_id(size_id)

    def get_ingredients(self, ingredient_ids):
        return IngredientManager.get_by_id_list(ingredient_ids)

    def get_beverages(self, beverage_ids):
        return BeverageManager.get_by_id_list(beverage_ids)

    def calculate_order_price(self, size_price, ingredients, beverages):
        price = sum(ingredient.price for ingredient in ingredients)
        price += size_price

        if beverages:
            price += sum(beverage.price for beverage in beverages)

        return round(price, 2)

    def create_order(self, order_with_price, ingredients, beverages):
        return self.manager.create(order_with_price, ingredients, beverages)
