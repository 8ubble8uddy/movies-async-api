from typing import ClassVar, List, Type
from uuid import UUID

from pydantic import BaseModel, Field

from models.base import OrjsonMixin, UUIDMixin


class GenreInFilm(BaseModel):
    """Модель жанра в фильме."""

    uuid: UUID = Field(alias='id')
    name: str

    class Config(OrjsonMixin.Config):
        """Настройки валидации."""

        allow_population_by_field_name = True


class PersonInFilm(BaseModel):
    """Модель персоны в фильме."""

    uuid: UUID = Field(alias='id')
    full_name: str = Field(alias='name')

    class Config(OrjsonMixin.Config):
        """Настройки валидации."""

        allow_population_by_field_name = True


class Film(UUIDMixin, OrjsonMixin):
    """Модель фильма с полной информацией."""

    title: str
    imdb_rating: float
    description: str
    genre: List[GenreInFilm]
    actors: List[PersonInFilm]
    writers: List[PersonInFilm]
    directors: List[PersonInFilm]


class FilmModified(UUIDMixin, OrjsonMixin):
    """Модель фильма с краткой информацией."""

    title: str
    imdb_rating: float


class FilmList(OrjsonMixin):
    """Модель для парсирования списка фильмов с краткой информацией."""

    __root__: List[FilmModified]
    item: ClassVar[Type] = FilmModified
