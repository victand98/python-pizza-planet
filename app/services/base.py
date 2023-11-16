from typing import Any, Tuple, Union

from flask import Response, jsonify, request

from ..common import BAD_REQUEST, CREATED, NOT_FOUND, OK
from ..controllers import BaseController


class BaseService:
    def __init__(self, controller: BaseController) -> None:
        self.controller = controller

    def _handle_operation(
        self,
        result: Union[Any, None],
        error: Union[str, None],
        is_create: bool = False,
    ) -> Tuple[Response, int]:
        response = result if not error else {"error": error}
        if is_create:
            status_code = CREATED if not error else BAD_REQUEST
        else:
            status_code = OK if result else NOT_FOUND if not error else BAD_REQUEST
        return jsonify(response), status_code

    def create(self) -> Tuple[Response, int]:
        result, error = self.controller.create(request.json)
        return self._handle_operation(result, error, True)

    def update(self, _id: int) -> Tuple[Response, int]:
        result, error = self.controller.update(_id, request.json)
        return self._handle_operation(result, error)

    def get_by_id(self, _id: int) -> Tuple[Response, int]:
        result, error = self.controller.get_by_id(_id)
        return self._handle_operation(result, error)

    def get_all(self) -> Tuple[Response, int]:
        result, error = self.controller.get_all()
        return self._handle_operation(result, error)
