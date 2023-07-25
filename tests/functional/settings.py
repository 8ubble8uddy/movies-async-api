import logging
from typing import Optional, Type, Union

from pydantic import BaseModel, BaseSettings, Field, validator

from testdata.schemas.genre import Genre
from testdata.schemas.movie import Movie
from testdata.schemas.person import Person

Schema = Type[Union[Movie, Person, Genre]]
Document = Union[Movie, Person, Genre]

logging.basicConfig(level=logging.INFO)


class TestDBConfig(BaseModel):
    """Класс для валидации настроек подключения к тестовой базе данных."""

    host: str
    port: int


class RedisConfig(TestDBConfig):
    """Класс с настройками для подключения к Redis."""


class ElasticConfig(TestDBConfig):
    """Класс с настройками для подключения к Elasticsearch."""


class UrlPath(BaseModel):
    """Класс для предоставления URL-адреса сервиса."""

    protocol: str = Field(default='http://')
    domain: str = Field(default='127.0.0.1')
    port: int = Field(default=8000)
    api_path: str = Field(default='/api/v1')

    @validator('port')
    def get_port(cls, port: int) -> str:
        """
        Преобразование порта для корректного представления в URL-адресе.

        Args:
            port: Порт для подключения к сервису

        Returns:
            str: Порт в виде части URL-адреса
        """
        return f':{port}' if port not in {80, 443} else ''

    def __str__(self) -> str:
        """Строковое представление сформированного URL-адреса сервиса.

        Returns:
            str: URL-адрекс сервиса
        """
        return ''.join(value for _, value in self.__repr_args__())

    class Config:
        """Настройки валидации."""

        validate_all = True


class QueryParams(BaseModel):
    """Класс для предоставления параметров запроса в URL-адресе."""

    filter: Optional[str] = Field(alias='filter[genre]')
    page_number: Optional[int] = Field(default=1, alias='page[number]')
    page_size: Optional[int] = Field(default=50, alias='page[size]')
    query: Optional[str]
    sort: Optional[str]

    class Config:
        """Настройки валидации."""

        allow_population_by_field_name = True


class TestMainSettings(BaseSettings):
    """Класс с настройками для тестирования проекта."""

    secret_key: str = Field(default='secret_key')
    url: UrlPath = Field(default_factory=UrlPath)
    elastic: TestDBConfig = Field(default=ElasticConfig(host='127.0.0.1', port=9200))
    redis: TestDBConfig = Field(default=RedisConfig(host='127.0.0.1', port=6379))


TEST_CONFIG = TestMainSettings(_env_file='.env', _env_nested_delimiter='_')
MAX_PAGE_SIZE = 100
MAX_TIME_CONNECTION = 15
