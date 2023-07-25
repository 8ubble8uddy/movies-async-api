import abc
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from services.base import BaseService
from db import queries


class BaseFilter(BaseModel, abc.ABC):
    """Абстрактный класс фильтра данных кинотеатра."""

    def __new__(cls, **kwargs):
        """
        При создании объекта возвращет None, если отсутствуют данные для фильтрации.

        Args:
            kwargs: Именнованные аргументы для создания объекта

        Returns:
            Optional['BaseFilter']: Объект фильтра либо None
        """
        return super().__new__(cls) if all(kwargs.values()) else None


class FilterFilms(BaseFilter):
    """Абстрактный класс фильтра фильмов."""

    id: Optional[UUID]

    @abc.abstractmethod
    async def get_query(self, service: BaseService) -> Dict:
        """Получить данные и запрос для фильтрации данных.

        Args:
            service: Сервис, выполняющий бизнес-логику с фильмами
        """

    def __str__(self) -> str:
        """
        Строковое представление в виде ID объекта по которому выполняется фильтрация.

        Returns:
            str: ID объекта для фильтрации
        """
        return str(self.id)


class FilterGenreFilms(FilterFilms):
    """Класс фильтра фильмов по жанру."""

    id: Optional[UUID] = Field(alias='genre_id')

    async def get_query(self, service: BaseService) -> Dict:
        """
        Получение данных жанра и запроса для фильтрации по нему фильмов.

        Args:
            service: Сервис, выполняющий бизнес-логику с фильмами

        Returns:
            Dict: Запрос с фильтрацией по жанру
        """
        genre = await service.get_elastic_doc(index='genres', doc_id=self.id)
        return queries.films_by_genre(genre)


class FilterPersonFilms(FilterFilms):
    """Класс фильтра фильмов по персоне."""

    id: Optional[UUID] = Field(alias='person_id')

    async def get_query(self, service: BaseService) -> Dict:
        """
        Получение данных персоны и запроса для фильтрации по ней фильмов.

        Args:
            service: Сервис, выполняющий бизнес-логику с фильмами

        Returns:
            Dict: Запрос с фильтрацией по персоне
        """
        person = await service.get_elastic_doc(index='persons', doc_id=self.id)
        return queries.films_by_person(person, fields=['id', 'title', 'imdb_rating'])


class QuerySearch(BaseFilter):
    """Класс фильтра для полнотекстового поиска данных."""

    q_string: Optional[str]
    fields: List[str] = Field(default_factory=list)

    def __str__(self) -> str:
        """
        Строковое представление в виде переданной строки запроса.

        Returns:
            str: Строка запроса
        """
        return self.q_string or ''
