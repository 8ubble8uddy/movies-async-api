from functools import lru_cache
from typing import ClassVar, Union

from pydantic import BaseSettings, Field

from models.film import Film, FilmList, FilmModified
from models.genre import Genre, GenreList
from models.person import Person, PersonList

CinemaObject = Union[Film, FilmModified, Person, Genre]
CinemaObjectList = Union[FilmList, PersonList, GenreList]


class RedisConfig(BaseSettings):
    """Класс с настройками подключения к Redis."""

    host: str = '127.0.0.1'
    port: int = 6379


class ElasticConfig(BaseSettings):
    """Класс с настройками подключения к Elasticsearch."""

    host: str = '127.0.0.1'
    port: int = 9200


class LogstashConfig(BaseSettings):
    """Класс с настройками подключения к Logstash."""

    host: str = 'localhost'
    port: int = 5044


class FastApiConfig(BaseSettings):
    """Класс с настройками подключения к FastAPI."""

    host: str = '0.0.0.0'
    port: int = 8000
    debug: bool = False
    docs: str = 'openapi'
    secret_key: str = 'secret_key'
    project_name: str = 'Read-only API для онлайн-кинотеатра'
    cache_expire_in_seconds: ClassVar[int] = 60


class MainSettings(BaseSettings):
    """Класс с основными настройками проекта."""

    fastapi: FastApiConfig = Field(default_factory=FastApiConfig)
    elastic: ElasticConfig = Field(default_factory=ElasticConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    logstash: LogstashConfig = Field(default_factory=LogstashConfig)


@lru_cache()
def get_settings() -> MainSettings:
    """
    Функция для создания объекта настроек в едином экземпляре (синглтона).

    Returns:
        MainSettings: Объект с настройками
    """
    return MainSettings(_env_file='.env', _env_nested_delimiter='_')


CONFIG = get_settings()
