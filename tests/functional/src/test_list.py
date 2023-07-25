import http
from typing import Callable

import pytest


@pytest.mark.parametrize(
    'path, index',
    [
        ('/films', 'movies'),
        ('/persons', 'persons'),
        ('/genres', 'genres'),
    ],
)
@pytest.mark.asyncio
async def test_get_list(
    path: str, index: str,  # args
    make_get_request: Callable, check_cache: Callable,  # fixtures
):
    """
    Тестирование получения списка данных.

    Args:
        path: Путь к URL-ресурсу
        index: Название индекса Elasticsearch
        make_get_request: Фикстура, выполняющая HTTP-запрос
        check_cache: Фикстура, проверяющая кэш данных
    """
    response = await make_get_request(path)
    cache = await check_cache(index)

    assert response.status == http.HTTPStatus.OK
    assert cache
