import http
from typing import Callable

import pytest


@pytest.mark.parametrize(
    'path, index, check_field',
    [
        ('/films/{id}', 'movies', 'title'),
        ('/persons/{id}', 'persons', 'full_name'),
        ('/genres/{id}', 'genres', 'name'),
    ],
)
@pytest.mark.asyncio
async def test_get_by_id(
    path: str, index: str, check_field: str,  # args
    extract_data: Callable, make_get_request: Callable, check_cache: Callable,  # fixtures
):
    """
    Тестирование получения данных по ID.

    Args:
        path: Путь к URL-ресурсу
        index: Название индекса Elasticsearch
        check_field: Поле объекта по которому осуществляется проверка данных
        extract_data: Фикстура, извлекающая данные из БД
        make_get_request: Фикстура, выполняющая HTTP-запрос
        check_cache: Фикстура, проверяющая кэш данных
    """
    expected = await extract_data(index)

    response = await make_get_request(path.format(id=expected['id']))
    cache = await check_cache(index, id=expected['id'])

    assert response.status == http.HTTPStatus.OK
    assert response.body[check_field] == expected[check_field]
    assert cache
