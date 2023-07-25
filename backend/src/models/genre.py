from typing import ClassVar, List

from models.base import OrjsonMixin, UUIDMixin


class Genre(UUIDMixin, OrjsonMixin):
    """Модель жанра."""

    name: str
    description: str


class GenreList(OrjsonMixin):
    """Модель для парсирования списка жанров."""

    __root__: List[Genre]
    item: ClassVar[type] = Genre
