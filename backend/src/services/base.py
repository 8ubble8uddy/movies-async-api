import abc
from enum import Enum
from functools import wraps
from typing import Callable, Type, Union

from pydantic import BaseModel, parse_obj_as, parse_raw_as

from core.config import CinemaObject, CinemaObjectList
from db.elastic import ElasticStorage
from db.redis import RedisStorage


class ElasticIndices(Enum):
    """Индексы с данными кинотеатра в Elasticsearch."""

    movies = 'movies'
    persons = 'persons'
    genres = 'genres'


class BaseService(ElasticStorage, RedisStorage, abc.ABC):
    """Абстрактный класс сервиса для реализации бизнес-логики по работе с кинотеатром."""

    index: ElasticIndices
    model: Type[Union[CinemaObject, CinemaObjectList]]

    @property
    @abc.abstractmethod
    def redis_key(self) -> str:
        """Ключ от данных в кэше Redis в виде строки."""

    @abc.abstractmethod
    async def get(self) -> Union[CinemaObject, CinemaObjectList]:
        """Получить представление данных кинотеатра."""

    class Config:
        """Настройки валидиции."""

        use_enum_values = True


def redis_cache(expire: int) -> Callable:
    """
    Декоратор для получения и сохранения данных кинотеатра в кеше Redis.

    Args:
        expire: Время жизни кеша

    Returns:
        Callable: Декорируемая функция, получающая представление данных кинотетра
    """
    def decorator(get) -> Callable:
        @wraps(get)
        async def wrapper(*args, **kwargs) -> BaseModel:
            self: BaseService = args[0]
            data = await self.get_redis_value(self.redis_key)
            if not data:
                data = parse_obj_as(
                    self.model, obj=await get(*args, **kwargs),
                ).json()
                await self.set_redis_value(self.redis_key, data, expire=expire)
            return parse_raw_as(self.model, b=data)
        return wrapper
    return decorator
