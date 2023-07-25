from functools import lru_cache

from fastapi import Depends, Path, Query

from api.v1.base import Database, Paginator
from services.filters import FilterGenreFilms, QuerySearch
from services.list import ListService
from services.retrieve import RetrieveService
from models.film import Film, FilmList


@lru_cache()
def get_film_list(
    filter_genre: str = Query(default=None, alias='filter[genre]', description='Фильтр по жанру'),
    sort: str = Query(default=None, description='Параметр сортировки'),
    paginator: Paginator = Depends(),
    database: Database = Depends(),
) -> ListService:
    """
    Функция провайдер для ListService, чтобы получить список фильмов.

    Args:
        filter_genre: Фильтр по жанру
        sort: Параметр сортировки
        paginator: Пагинатор
        database: Подключения к базам данных

    Returns:
        ListService: Сервис для получения списка объектов кинотеатра
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='movies', model=FilmList,
        filter=FilterGenreFilms(genre_id=filter_genre),
        page_size=paginator.size, page_number=paginator.page, sort=sort,
    )


@lru_cache()
def get_film_search(
    query: str = Query(default=None, description='Поисковый запрос'),
    paginator: Paginator = Depends(),
    database: Database = Depends(),
) -> ListService:
    """
    Функция провайдер для ListService, чтобы получить результаты поиска по фильмам.

    Args:
        query: Поисковый запрос
        paginator: Пагинатор
        database: Подключения к базам данных

    Returns:
        ListService: Сервис для получения списка объектов кинотеатра
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='movies', model=FilmList,
        page_size=paginator.size, page_number=paginator.page,
        query=QuerySearch(q_string=query, fields=['title']),
    )


@lru_cache()
def get_film_details(
    film_id: str = Path(title='Фильм ID'),
    database: Database = Depends(),
) -> RetrieveService:
    """
    Функция провайдер для RetrieveService, чтобы получить фильм по ID.

    Args:
        film_id: ID фильма
        database: Подключения к базам данных

    Returns:
        RetrieveService: Сервис для получения объекта кинотеатра по ID
    """
    return RetrieveService(
        elastic=database.elastic, redis=database.redis,
        index='movies', model=Film, id=film_id,
    )
