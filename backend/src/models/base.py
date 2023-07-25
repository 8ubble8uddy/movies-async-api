from typing import Callable
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(value: object, *, default: Callable) -> str:
    """
    Функция для декодирования в unicode для парсирования объектов на основе pydantic класса.

    Args:
        value: Данные для преобразования
        default: Функция для объектов, которые не могут быть сериализованы.

    Returns:
        str: Строка JSON
    """
    return orjson.dumps(value, default=default).decode()


class UUIDMixin(BaseModel):
    """Миксин для хранения первичных ключей."""

    uuid: UUID


class OrjsonMixin(BaseModel):
    """Миксин для замены стандартной работы с json на более быструю."""

    class Config:
        """Настройки сериализации."""

        json_loads = orjson.loads
        json_dumps = orjson_dumps
