from typing import Optional

from aioredis import Redis
from aioredis.errors import ConnectionClosedError

from db.base import DatabaseModel
from core.decorators import backoff

connection: Optional[Redis] = None


async def get_redis() -> Redis:
    """
    Функция для объявления соединения с Redis, которая понадобится при внедрении зависимостей.

    Returns:
        Redis: Соединение с Redis
    """
    return connection


class RedisStorage(DatabaseModel):
    """Класс для работы с хранилищем Redis в виде кэша данных."""

    redis: Redis

    @backoff(errors=(ConnectionClosedError))
    async def get_redis_value(self, key: str) -> bytes:
        """
        Получить данных из кэша Redis.

        Args:
            key: Ключ от данных

        Returns:
            bytes: Данные из кэша
        """
        value = await self.redis.get(key=key)
        return value

    @backoff(errors=(ConnectionClosedError))
    async def set_redis_value(self, key: str, data: str, **kwargs):
        """
        Записать данные в кэш Redis.

        Args:
            key: Ключ от данных
            data: Данные для записи
            kwargs: Необязательные именованные аргументы
        """
        await self.redis.set(key, data, **kwargs)
