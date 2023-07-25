import random
from typing import AsyncGenerator, Callable, Dict, List, Optional
from uuid import UUID

import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from settings import TEST_CONFIG


@pytest_asyncio.fixture(scope='session')
async def elastic() -> AsyncGenerator[AsyncElasticsearch, None]:
    """
    Фикстура для подключения к Elasticsearch и очищения данных БД после тестов.

    Yields:
        AsyncElasticsearch: Объект для асинхронной работы с Elasticsearch
    """
    elastic = AsyncElasticsearch(
        hosts='{host}:{port}'.format(**TEST_CONFIG.elastic.dict()),
    )
    try:
        yield elastic
    finally:
        await elastic.indices.delete('_all')
        await elastic.close()


def get_random_doc(data: List[Dict]) -> Dict:
    """
    Получения случайного элемента из списка.

    Args:
        data: Список с документами из Elasticsearch

    Returns:
        dict: Случайный документ
    """
    docs = [doc['_source'] for doc in data['hits']['hits']]  # type: ignore[call-overload]
    return docs[random.randrange(len(docs))] if docs else {}


@pytest.fixture(scope='session')
def extract_data(elastic: AsyncElasticsearch) -> Callable:
    """
    Фикстура с вложенной функцией для получения данных из БД.

    Args:
        elastic: Фикстура с клиентом Elasticsearch

    Returns:
        Callable: Фикстура-функция, чтобы получить данные из БД Elasticsearch
    """
    async def inner(index: str, id: Optional[UUID] = None) -> dict:
        if not id:
            data = await elastic.search(index=index, size=1000)
            return get_random_doc(data)
        return await elastic.get_source(index=index, id=id)
    return inner
