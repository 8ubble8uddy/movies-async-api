from typing import AsyncGenerator, Callable, Optional
from uuid import UUID

import aioredis
import pytest
import pytest_asyncio

from settings import TEST_CONFIG, QueryParams


@pytest_asyncio.fixture(scope='session')
async def redis() -> AsyncGenerator[aioredis.Redis, None]:
    """
    Фикстура для подключения к Redis и очищения кэша данных после тестов.

    Yields:
        aioredis.Redis: Объект для асинхронной работы с Redis
    """
    redis = await aioredis.create_redis_pool(
        tuple(TEST_CONFIG.redis.dict().values()), minsize=10, maxsize=20,
    )
    try:
        yield redis
    finally:
        await redis.flushall()
        redis.close()
        await redis.wait_closed()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def clear_cache(redis: aioredis.Redis):
    """
    Фикстура для очищения кэша перед запуском тестов.

    Args:
        redis: Фикстура с клиентом Redis
    """
    await redis.flushall()


def get_redis_key(index: str, id: Optional[UUID], **kwargs) -> str:
    """
    Получение ключа от данных в кэше Redis.

    Args:
        index: Название индекса Elasticsearch
        id: ID данных
        kwargs: Именованные параметры запроса в URL-адресе

    Returns:
        str: Ключ от данных в Redis
    """
    params = [
        f'{field}::{value}' for field, value in QueryParams(**kwargs).dict().items()
    ]
    if id:
        return '{index}::id::{id}'.format(index=index, id=id)
    return '{index}::{params}'.format(index=index, params='::'.join(params))


@pytest.fixture(scope='session')
def check_cache(redis: aioredis.Redis) -> Callable:
    """
    Фикстура с вложенной функцией для получения данных из кэша.

    Args:
        redis: Фикстура с клиентом Redis

    Returns:
        Callable: Фикстура-функция, чтобы получить данные из кэша Redis
    """
    async def inner(index: str, id: Optional[UUID] = None, **kwargs) -> bytes:
        cache = await redis.get(
            key=get_redis_key(index=index, id=id, **kwargs),
        )
        return cache
    return inner
