from typing import AsyncGenerator, Callable, Dict, List, Union

import aiohttp
import jwt
import pytest
import pytest_asyncio
from multidict import CIMultiDictProxy
from pydantic import BaseModel

from settings import TEST_CONFIG, QueryParams


class HttpResponse(BaseModel):
    """Класс HTTP-ответа сервера на запрос клиента."""

    body: Union[Dict, List[Dict]]
    headers: CIMultiDictProxy
    status: int

    class Config:
        arbitrary_types_allowed = True


@pytest_asyncio.fixture(scope='session')
async def session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """
    Фикстура для создании HTTP-сессии между сервером и клиентом.

    Yields:
        aiohttp.ClientSession: Объект для асинхронной работы с HTTP
    """
    token = jwt.encode({'some': 'payload'}, TEST_CONFIG.secret_key, algorithm='HS256')
    session = aiohttp.ClientSession(headers={'Authorization': f'Bearer {token}'})
    try:
        yield session
    finally:
        await session.close()


def get_url_path(path: str) -> str:
    """
    Получение URL-адреса ресурса без параметров запроса.

    Args:
        path: Путь к ресурсу

    Returns:
        str: URL-адрес
    """
    return '{url}{path_to_resource}'.format(url=TEST_CONFIG.url, path_to_resource=path)


def get_query_params(**params) -> Dict:
    """
    Получение и форматирование параметров запроса к URL-адресу.

    Args:
        params: Именованные параметры запроса

    Returns:
        Dict: Параметры запроса в URL-адресе
    """
    return QueryParams(**params).dict(by_alias=True, exclude_none=True)


@pytest.fixture(scope='session')
def make_get_request(session: aiohttp.ClientSession) -> Callable:
    """
    Фикстура с вложенной функцией для получения данных от сервера.

    Args:
        session: Фикстура с HTTP-клиентом

    Returns:
        Callable: Фикстура-функция, чтобы получить данных от HTTP-сервера
    """
    async def inner(path: str, **params) -> HttpResponse:
        async with session.get(
            url=get_url_path(path=path),
            params=get_query_params(**params),
        ) as response:
            return HttpResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner
