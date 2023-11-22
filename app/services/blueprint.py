from typing import Tuple

from flask import Blueprint, Response

from ..common import GET, POST, PUT
from ..controllers import BaseController
from .base import BaseService


class BaseBlueprint(Blueprint):
    def __init__(
        self, name: str, import_name: str, controller: BaseController, **kwargs
    ) -> None:
        super().__init__(name, import_name, **kwargs)
        self.service = BaseService(controller)
        self._register_routes()

    def _register_routes(self) -> None:
        self.add_url_rule("/", methods=POST, view_func=self.create)
        self.add_url_rule("/<_id>", methods=PUT, view_func=self.update)
        self.add_url_rule("/<_id>", methods=GET, view_func=self.get_by_id)
        self.add_url_rule("/", methods=GET, view_func=self.get_all)

    def create(self) -> Tuple[Response, int]:
        return self.service.create()

    def update(self, _id: int) -> Tuple[Response, int]:
        return self.service.update(_id)

    def get_by_id(self, _id: int) -> Tuple[Response, int]:
        return self.service.get_by_id(_id)

    def get_all(self) -> Tuple[Response, int]:
        return self.service.get_all()
