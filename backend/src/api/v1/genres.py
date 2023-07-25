from functools import lru_cache

from fastapi import Depends, Path

from api.v1.base import Database, Paginator
from services.list import ListService
from services.retrieve import RetrieveService
from models.genre import Genre, GenreList


@lru_cache()
def get_genre_list(
    paginator: Paginator = Depends(),
    database: Database = Depends(),
) -> ListService:
    """
    Функция провайдер для ListService, чтобы получить список жанров.

    Args:
        paginator: Пагинатор
        database: Подключения к базам данных

    Returns:
        ListService: Сервис для получения списка объектов кинотеатра
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='genres', model=GenreList,
        page_size=paginator.size, page_number=paginator.page,
    )


@lru_cache()
def get_genre_details(
    genre_id: str = Path(title='Жанр ID'),
    database: Database = Depends(),
) -> RetrieveService:
    """
    Функция провайдер для RetrieveService, чтобы получить жанр по ID.

    Args:
        genre_id: ID жанра
        database: Подключения к базам данных

    Returns:
        RetrieveService: Сервис для получения объекта кинотеатра по ID
    """
    return RetrieveService(
        elastic=database.elastic, redis=database.redis,
        index='genres', model=Genre, id=genre_id,
    )
