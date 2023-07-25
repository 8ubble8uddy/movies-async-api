from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends, Query

from db.elastic import get_elastic
from db.redis import get_redis


class Paginator:
    """Класс для получения запроса страницы."""

    def __init__(
        self,
        page_number: int = Query(default=1, alias='page[number]', description='Номер страницы', ge=1),
        page_size: int = Query(default=50, alias='page[size]', description='Размер страницы', ge=1, le=100),
    ):
        """
        При инициализации класса принимает в запросе параметры номера страницы и её размера.

        Args:
            page_number: Номер страницы
            page_size: Размер страницы
        """
        self.page = page_number
        self.size = page_size


class Database:
    """Класс с зависимостями для работы с базами данных Elasticsearch и Redis."""

    def __init__(
        self,
        elastic: AsyncElasticsearch = Depends(get_elastic),
        redis: Redis = Depends(get_redis),
    ):
        """
        При инициализации класса внедряет зависимости от подключений к Elasticsearch и Redis.

        Args:
            elastic: Подключение к Elasticsearch для хранения данных
            redis: Подключение к Redis для кеширования данных
        """
        self.redis = redis
        self.elastic = elastic
