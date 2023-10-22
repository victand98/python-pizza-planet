from app.common.http_methods import GET, POST
from flask import Blueprint

from ..controllers import OrderController
from .base import BaseService

order = Blueprint('order', __name__)
order_controller = OrderController()


@order.route('/', methods=POST)
def create_order():
    return BaseService.create(order_controller)


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    return BaseService.get_by_id(order_controller, _id)


@order.route('/', methods=GET)
def get_orders():
    return BaseService.get_all(order_controller)
