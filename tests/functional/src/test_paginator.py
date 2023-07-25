from typing import Callable, List, Tuple

import pytest

from conftest import GENRES_COUNT, MOVIES_COUNT, PERSONS_COUNT
from settings import MAX_PAGE_SIZE


def paginate(total_items: int) -> List[Tuple]:
    """
    Получение параметров страницы и размера.

    Args:
        total_items: Общее количество элементов

    Returns:
        list[tuple]: Параметры номера страницы и её размера
    """
    max_count = total_items if total_items < MAX_PAGE_SIZE else MAX_PAGE_SIZE
    return [
        (1, max_count),
        (2, max_count // 2),
        (3, max_count // 4),
    ]


@pytest.mark.parametrize(
    'path, paginator',
    [
        ('/films', paginate(MOVIES_COUNT)),
        ('/persons', paginate(PERSONS_COUNT)),
        ('/genres', paginate(GENRES_COUNT)),
    ],
)
@pytest.mark.asyncio
async def test_get_page(
    path: str, paginator: List[Tuple],  # args
    make_get_request: Callable,  # fixtures
):
    """
    Тестирование постраничного разбиения данных.

    Args:
        path: Путь к URL-ресурсу
        paginator: Список параметров с номером страницы и её размером
        make_get_request: Фикстура, выполняющая HTTP-запрос
    """
    for page, expected_size in paginator:
        response = await make_get_request(path, page_number=page, page_size=expected_size)
        assert len(response.body) == expected_size
