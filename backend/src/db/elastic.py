from http import HTTPStatus
from typing import Dict, List, Optional
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.exceptions import ConnectionError
from fastapi import HTTPException

from db.base import DatabaseModel
from core.decorators import backoff

connection: Optional[AsyncElasticsearch] = None


async def get_elastic() -> AsyncElasticsearch:
    """
    Функция для объявления соединения с Elasticsearch, которая понадобится при внедрении зависимостей.

    Returns:
        AsyncElasticsearch: Соединение с Elasticsearch
    """
    return connection


class ElasticStorage(DatabaseModel):
    """Класс для работы с хранилищем Elasticsearch в виде основной базы данных."""

    elastic: AsyncElasticsearch

    @backoff(errors=(ConnectionError))
    async def get_elastic_doc(self, index: str, doc_id: UUID) -> Dict:
        """
        Получение документа из Elasticsearch.

        Args:
            index: Индекс c документами
            doc_id: ID документа

        Raises:
            HTTPException: Если документа нет, то отдаём HTTP-статус 404

        Returns:
            Dict: Данные документа без информации о результатах запроса
        """
        try:
            doc = await self.elastic.get(index=index, id=doc_id)
        except NotFoundError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        return doc['_source']

    @backoff(errors=(ConnectionError))
    async def search_elastic_docs(self, index: str, queryset: Optional[Dict] = None) -> List[Dict]:
        """
        Получение списка документов из Elasticsearch.

        Args:
            index: Индекс с документами
            queryset: Параметры запроса для поиска данных

        Raises:
            HTTPException: Если по запросу нет документов, то отдаём HTTP-статус 404

        Returns:
            List[dict]: Список данных документов без информации о результатах запроса
        """
        try:
            docs = await self.elastic.search(index=index, **queryset or {})
        except NotFoundError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        return [doc['_source'] for doc in docs['hits']['hits']]
