from typing import Callable, Dict, List

import pytest


def persons_names(film: Dict) -> List[str]:
    """
    Получение списка с именами персон фильма.

    Args:
        film: Фильм с персонами

    Returns:
        list[str]: Список имён персон
    """
    return film['actors_names'] + film['writers_names'] + film['director']


def genres_names(film: Dict) -> List[str]:
    """
    Получение списка с названиями жанров фильма.

    Args:
        film: Фильм с жанрами

    Returns:
        list[str]: Список названий жанров
    """
    return film['genre']


@pytest.mark.parametrize(
    'path, index, check_field, check_list',
    [
        ('/films?filter[genre]={id}', 'genres', 'name', genres_names),
        ('/persons/{id}/film', 'persons', 'full_name', persons_names),
    ],
)
@pytest.mark.asyncio
async def test_films_filters(
    path: str, index: str, check_field: str, check_list: Callable,  # args
    extract_data: Callable, make_get_request: Callable,  # fixtures
):
    """
    Тестирование фильтров для фильмов.

    Args:
        path: Путь к URL-ресурсу
        index: Название индекса Elasticsearch
        check_field: Поле объекта по которому осуществляется фильтрация
        check_list: Функция, возвращающая список, по которому проверяется наличие объекта
        extract_data: Фикстура, извлекающая данные из БД
        make_get_request: Фикстура, выполняющая HTTP-запрос
    """
    expected = await extract_data(index)

    response = await make_get_request(path=path.format(id=expected['id']))
    film = await extract_data(index='movies', id=response.body[0]['uuid'])

    assert expected[check_field] in check_list(film)
