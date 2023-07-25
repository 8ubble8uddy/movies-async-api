from typing import Callable, List

import pytest


def asc(data: List[float]) -> bool:
    """
    Возвращает `True` если числа в списке располагаются в порядке возрастания.

    Args:
        data: Спсок чисел с плавающей точкой

    Returns:
        bool: Булево значение
    """
    return all(prev <= next for prev, next in zip(data, data[1:]))


def desc(data: List[float]) -> bool:
    """
    Возвращает `True` если числа в списке располагаются в порядке убывания.

    Args:
        data: Спсок чисел с плавающей точкой

    Returns:
        bool: Булево значение
    """
    return all(prev >= next for prev, next in zip(data, data[1:]))


@pytest.mark.parametrize(
    'sort, ordering',
    [
        ('imdb_rating', asc),
        ('-imdb_rating', desc),
    ],
)
@pytest.mark.asyncio
async def test_films_sorting(
    sort: str, ordering: Callable,  # args
    make_get_request: Callable,  # fixtures
):
    """
    Тестирование сортировки фильмов по рейтингу.

    Args:
        sort: Поле фильма с его рейтингом
        ordering: Функция, возвращающая булево значение, на соответствие порядка элементов
        make_get_request: Фикстура, выполняющая HTTP-запрос
    """
    response = await make_get_request(path='/films', sort=sort)
    sorted_by = sort[1:] if sort.startswith('-') else sort

    assert response.body
    assert ordering([film[sorted_by] for film in response.body])
