from enum import Enum
from typing import ClassVar, List
from uuid import UUID

from models.base import OrjsonMixin, UUIDMixin


class RoleChoices(Enum):
    """Вспомогательная модель для соответствия названия поля в Elasticsearch и ролью персоны."""

    actors_names = 'actor'
    writers_names = 'writer'
    director = 'director'


class Person(UUIDMixin, OrjsonMixin):
    """Модель персоны с основной ролью и фильмами с его участием."""

    full_name: str
    role: str
    film_ids: List[UUID]


class PersonList(OrjsonMixin):
    """Модель для парсирования списка персон с информацией об их ролях и фильмах."""

    __root__: List[Person]
    item: ClassVar[type] = Person
