from functools import lru_cache

from fastapi import Depends, Path, Query

from api.v1.base import Database, Paginator
from services.filters import FilterPersonFilms, QuerySearch
from services.list import ListService
from services.retrieve import RetrieveService
from models.film import FilmList
from models.person import Person, PersonList


@lru_cache()
def get_person_list(
    paginator: Paginator = Depends(),
    database: Database = Depends(),
) -> ListService:
    """
    Функция провайдер для ListService, чтобы получить список персон.

    Args:
        paginator: Пагинатор
        database: Подключения к базам данных

    Returns:
        ListService: Сервис для получения списка объектов кинотеатра
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='persons', model=PersonList,
        page_size=paginator.size, page_number=paginator.page,
    )


@lru_cache()
def get_person_search(
    query: str = Query(default=None, description='Поисковый запрос'),
    paginator: Paginator = Depends(),
    database: Database = Depends(),
) -> ListService:
    """
    Функция провайдер для ListService, чтобы получить результаты поиска по персонам.

    Args:
        query: Поисковый запрос
        paginator: Пагинатор
        database: Подключения к базам данных

    Returns:
        ListService: Сервис для получения списка объектов кинотеатра
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='persons', model=PersonList,
        page_size=paginator.size, page_number=paginator.page,
        query=QuerySearch(q_string=query, fields=['full_name']),
    )


@lru_cache()
def get_person_films(
    person_id: str = Path(title='Персона ID'),
    database: Database = Depends(),
) -> ListService:
    """
    Функция провайдер для ListService, чтобы получить фильмы по персоне.

    Args:
        person_id: ID персоны для фильтрации фильмов
        database: Подключения к базам данных

    Returns:
        ListService: Сервис для получения списка объектов кинотеатра
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='movies', model=FilmList,
        filter=FilterPersonFilms(person_id=person_id),
    )


@lru_cache()
def get_person_details(
    person_id: str = Path(title='Персона ID'),
    database: Database = Depends(),
) -> RetrieveService:
    """
    Функция провайдер для RetrieveService, чтобы получить персону по ID.

    Args:
        person_id: ID персоны
        database: Подключения к базам данных

    Returns:
        RetrieveService: Сервис для получения объекта кинотеатра по ID
    """
    return RetrieveService(
        elastic=database.elastic, redis=database.redis,
        index='persons', model=Person, id=person_id,
    )
