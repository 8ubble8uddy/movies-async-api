from typing import Dict, List, Optional, Type

from pydantic import BaseModel

from services.filters import FilterFilms, QuerySearch
from core.config import CinemaObject
from db import queries
from models.film import Film
from models.person import Person, RoleChoices


class SingleObjectMixin(BaseModel):
    """Миксин для формирования объекта кинотеатра из базы данных Elasticsearch."""

    async def get_object(self, data: Dict, model: Type[CinemaObject]) -> CinemaObject:
        """
        Получение объекта и добор данных из других индексов Elasticsearch для соответствующей модели.

        Args:
            data: Данные для обработки
            model: Модель по которой нужно получить объект

        Returns:
            CinemaObject: Объект кинотеатра
        """
        if model == Film:
            data.update(await self.add_to_film(data))
        elif model == Person:
            data.update(await self.add_to_person(data))
        return model(uuid=data['id'], **data)

    async def add_to_film(self, film: Dict) -> Dict:
        """
        Добавление к данным фильма информации о его жанрах и режиссёрах из соответствующих индексов.

        Args:
            film: Данные фильма

        Returns:
            Dict: Жанры и режиссёры фильма
        """
        genres = await self.search_elastic_docs(  # type: ignore[attr-defined]
            index='genres', queryset={'body': queries.genres_by_film(film)},
        )
        directors = await self.search_elastic_docs(  # type: ignore[attr-defined]
            index='persons', queryset={'body': queries.directors_by_film(film)},
        )
        return {'genre': genres, 'directors': directors}

    async def add_to_person(self, person: Dict) -> Dict:
        """
        Добавление к данным персоны информации о его роли и фильмах из соответствующего индекса.

        Args:
            person: Данные персоны

        Returns:
            Dict: Роль и ID фильмов с участием персоны
        """
        films = await self.search_elastic_docs(  # type: ignore[attr-defined]
            index='movies', queryset={'body': queries.films_by_person(
                person, fields=['id', 'actors_names', 'writers_names', 'director'],
            )},
        )
        return {
            'film_ids': [film['id'] for film in films],
            'role': self.parse_role(person['full_name'], films),
        }

    def parse_role(self, person_name: str, films: List[Dict]) -> str:
        """
        Обработка фильмов с участием персоны для определения его основной роли.

        Args:
            person_name: Полное имя персоны
            films: Список фильмов с участием персоны

        Returns:
            str: Роль персоны, которая больше всего встречается в фильмах с его участием
        """
        person_roles = [
            RoleChoices[role].value
            for film in films if film.pop('id')
            for role, names in film.items() if person_name in names
        ]
        return max(person_roles, key=person_roles.count, default='')


class QuerysetMixin(BaseModel):
    """Миксин для формирования запроса к базе данных ElasticSearch."""

    filter: Optional[FilterFilms]
    page_number: Optional[int]
    page_size: Optional[int]
    query: Optional[QuerySearch]
    sort: Optional[str]

    def get_queryset(self) -> Dict:
        """
        Создание запроса для получение данных в Elasticsearch.

        Returns:
            Dict: Запрос с сортировкой данных
        """
        queryset: Dict = {}
        if self.sort:
            queryset.update(
                sort=f'{self.sort[1:]}:desc' if self.sort.startswith('-') else self.sort,
            )
        return queryset

    async def filter_queryset(self, queryset: Dict) -> Dict:
        """
        Добавление к запросу параметров для фильтрации данных или полнотекстового поиска.

        Args:
            queryset: Запрос в Elasticsearch

        Returns:
            Dict: Запрос с фильтрацией или поиском данных
        """
        if self.filter:
            queryset.update(
                body=await self.filter.get_query(service=self),  # type: ignore[arg-type]
            )
        elif self.query:
            queryset.update(
                body=queries.search_data(query_str=str(self.query), fields=self.query.fields),
            )
        return queryset

    def paginate_queryset(self, queryset: Dict) -> Dict:
        """
        Добавление к запросу параметров для постраничного разбиения объектов кинотеатра.

        Args:
            queryset: Запрос в Elasticsearch

        Returns:
            Dict: Запрос с получением страницы
        """
        if (page := self.page_number) and (size := self.page_size):
            queryset.update(
                from_=(page - 1) * size if page > 1 else 0,
                size=size,
            )
        return queryset
