from typing import Callable

import pytest


@pytest.mark.parametrize(
    'path, index, search_field',
    [
        ('/films/search', 'movies', 'title'),
        ('/persons/search', 'persons', 'full_name'),
    ],
)
@pytest.mark.asyncio
async def test_get_search(
    path: str, index: str, search_field: str,  # args
    extract_data: Callable, make_get_request: Callable, check_cache: Callable,  # fixtures
):
    """
    Тестирование полнотекстового поиска.

    Args:
        path: Путь к URL-ресурсу
        index: Название индекса Elasticsearch
        search_field: Поле объекта по которому осуществляется поиск
        extract_data: Фикстура, извлекающая данные из БД
        make_get_request: Фикстура, выполняющая HTTP-запрос
        check_cache: Фикстура, проверяющая кэш данных
    """
    expected = await extract_data(index)

    response = await make_get_request(path, query=expected[search_field])
    cache = await check_cache(index, query=expected[search_field])

    assert expected[search_field] in {data[search_field] for data in response.body}
    assert cache
