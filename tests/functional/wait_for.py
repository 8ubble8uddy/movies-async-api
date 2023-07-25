import time
from functools import wraps
from typing import Callable, List, Union

from elasticsearch import Elasticsearch, helpers, RequestError
from redis import Redis

from settings import Document, logging, MAX_TIME_CONNECTION, Schema, TEST_CONFIG
from testdata.factory import ElasticDocsFactory


def ping(client: Union[Elasticsearch, Redis]) -> Union[Elasticsearch, Redis]:
    """
    Проверка соединения c базой данных.

    Args:
        client: Клиент базы данных

    Raises:
        ConnectionError: Если нет ответа, поднимаем ошибку соединения

    Returns:
        Elasticsearch | Redis: Клиент с соединением
    """
    if not client.ping():
        raise ConnectionError('Отсутствует подключение к базе данных.')
    return client


def connecting(max_time: int, message: str, start_sleep_time=1, factor=2) -> Callable:
    """
    Декоратор для подключения клиента к базе данных и обработки неудачного подключения.

    Args:
        max_time: Время в секундах, отведенное на попытки соединения
        message: Сообщение об ошибке, если не удалось подключиться
        start_sleep_time: Начальное время повтора
        factor: Во сколько раз нужно увеличить время ожидания

    Returns:
        Callable: Декорируемая функция
    """
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Union[Elasticsearch, Redis]:  # type: ignore[return]
            delay = start_sleep_time
            while True:
                try:
                    pong = ping(client=func(*args, **kwargs))
                except ConnectionError:
                    if delay > max_time:
                        logging.error(message)
                        break
                    delay *= factor
                    time.sleep(delay)
                else:
                    return pong
        return wrapper
    return decorator


@connecting(max_time=MAX_TIME_CONNECTION, message='Не удалось подключиться к Elasticsearch.')
def get_elastic(host: str, port: int) -> Elasticsearch:
    """
    Получение объекта для работы с хранилищем Elasticsearch.

    Args:
        host: Хост
        port: Порт

    Returns:
        Elasticsearch: Клиент базы данных Elasticsearch
    """
    return Elasticsearch(f'{host}:{port}', validate_cert=False, use_ssl=False)


@connecting(max_time=MAX_TIME_CONNECTION, message='Не удалось подключиться к Redis.')
def get_redis(host: str, port: int) -> Redis:
    """
    Получение объекта для работы с кэшом Redis.

    Args:
        host: Хост
        port: Порт

    Returns:
        Redis: Клиент базы данных Redis
    """
    return Redis(host=host, port=port)


def create_indices(elastic: Elasticsearch, schemas: List[Schema]):
    """
    Функция для создания индексов в Elasticsearch.

    Args:
        elastic: Клиент для выполнения Elasticsearch-запросов
        schemas: Схемы индексов
    """
    for schema in schemas:
        try:
            elastic.indices.create(
                index=schema._index._name,
                body=schema._index.to_dict(),
            )
        except RequestError as exc:
            logging.error(exc)
        else:
            logging.info('Cоздан индекс {index_name}.'.format(index_name=schema._index._name))


def load_data(elastic: Elasticsearch, docs: List[Document]):
    """
    Функция для загрузки данных в Elasticsearch.

    Args:
        elastic: Клиент для выполнения Elasticsearch-запросов
        docs: Данные для загрузки
    """
    helpers.bulk(
        client=elastic,
        actions=(doc.to_dict() for doc in docs),
        refresh=True,
    )
    logging.info('Данные загружены.')


def clear_cache(redis: Redis):
    """
    Очистка кэша данных в Redis.

    Args:
        redis: Клиент для выполнения Redis-запросов
    """
    redis.flushall()
    logging.info('Кэш очищен.')


def main():
    """Функция с основной логикой работы программы."""
    with get_elastic(**TEST_CONFIG.elastic.dict()) as elastic:
        with get_redis(**TEST_CONFIG.redis.dict()) as redis:
            factory = ElasticDocsFactory()
            create_indices(elastic, factory.SCHEMAS)
            load_data(elastic, factory.gendata())
            clear_cache(redis)


if __name__ == '__main__':
    main()
