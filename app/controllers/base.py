from typing import Any, Optional, Tuple

from sqlalchemy.exc import SQLAlchemyError

from ..repositories import BaseManager


class BaseController:
    manager: Optional[BaseManager] = None

    @classmethod
    def get_by_id(cls, _id: Any) -> Tuple[Any, Optional[str]]:
        try:
            return cls.manager.get_by_id(_id), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)

    @classmethod
    def get_all(cls) -> Tuple[Any, Optional[str]]:
        try:
            return cls.manager.get_all(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)

    @classmethod
    def create(cls, entry: dict) -> Tuple[Any, Optional[str]]:
        try:
            return cls.manager.create(entry), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)

    @classmethod
    def update(cls, _id: Any, new_values: dict) -> Tuple[Any, Optional[str]]:
        try:
            if not _id:
                return None, "Error: No id was provided for update"
            return cls.manager.update(_id, new_values), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
