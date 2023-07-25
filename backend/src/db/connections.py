import logging

import aioredis
from elasticsearch import AsyncElasticsearch, RequestError

from core.config import CONFIG
from db import elastic, redis

SETTINGS = {
    'refresh_interval': '1s',
    'analysis': {
        'filter': {
            'english_stop': {'type': 'stop', 'stopwords': '_english_'},
            'english_stemmer': {'type': 'stemmer', 'language': 'english'},
            'english_possessive_stemmer': {'type': 'stemmer', 'language': 'possessive_english'},
            'russian_stop': {'type': 'stop', 'stopwords': '_russian_'},
            'russian_stemmer': {'type': 'stemmer', 'language': 'russian'},
        },
        'analyzer': {
            'ru_en': {'tokenizer': 'standard', 'filter': [
                'lowercase',
                'english_stop',
                'english_stemmer',
                'english_possessive_stemmer',
                'russian_stop',
                'russian_stemmer',
            ]},
        },
    },
}


async def create_movies_index():
    """Функция для создания индекса с фильмами."""
    try:
        await elastic.connection.indices.create(
            index='movies',
            body={
                'settings': SETTINGS,
                'mappings': {
                    'dynamic': 'strict',
                    'properties': {
                        'id': {'type': 'keyword'},
                        'imdb_rating': {'type': 'float'},
                        'genre': {'type': 'keyword'},
                        'title': {'type': 'text', 'analyzer': 'ru_en', 'fields': {'raw': {'type': 'keyword'}}},
                        'description': {'type': 'text', 'analyzer': 'ru_en'},
                        'director': {'type': 'text', 'analyzer': 'ru_en'},
                        'actors_names': {'type': 'text', 'analyzer': 'ru_en'},
                        'writers_names': {'type': 'text', 'analyzer': 'ru_en'},
                        'actors': {'type': 'nested', 'dynamic': 'strict', 'properties': {
                            'id': {'type': 'keyword'},
                            'name': {'type': 'text', 'analyzer': 'ru_en'},
                        }},
                        'writers': {'type': 'nested', 'dynamic': 'strict', 'properties': {
                            'id': {'type': 'keyword'},
                            'name': {'type': 'text', 'analyzer': 'ru_en'},
                        }},
                    },
                },
            },
        )
    except RequestError as exc:
        logging.error(exc)
    else:
        logging.info('Создан индекс с фильмами.')


async def create_persons_index():
    """Функция для создания индекса с персонами."""
    try:
        await elastic.connection.indices.create(
            index='persons',
            body={
                'settings': SETTINGS,
                'mappings': {
                    'dynamic': 'strict',
                    'properties': {
                        'id': {'type': 'keyword'},
                        'full_name': {'type': 'text', 'analyzer': 'ru_en', 'fields': {'raw': {'type': 'keyword'}}},
                    },
                },
            },
        )
    except RequestError as exc:
        logging.error(exc)
    else:
        logging.info('Создан индекс с персонами.')


async def create_genres_index():
    """Функция для создания индекса с жанрами."""
    try:
        await elastic.connection.indices.create(
            index='genres',
            body={
                'settings': SETTINGS,
                'mappings': {
                    'dynamic': 'strict',
                    'properties': {
                        'id': {'type': 'keyword'},
                        'name': {'type': 'text', 'analyzer': 'ru_en', 'fields': {'raw': {'type': 'keyword'}}},
                        'description': {'type': 'text', 'analyzer': 'ru_en'},
                    },
                },
            },
        )
    except RequestError as exc:
        logging.error(exc)
    else:
        logging.info('Создан индекс с жанрами.')


async def start_elasticsearch():
    """Корутина для подключение к базе данных Elasticsearch."""
    elastic.connection = AsyncElasticsearch(
        hosts=['{host}:{port}'.format(host=CONFIG.elastic.host, port=CONFIG.elastic.port)],
    )


async def start_redis():
    """Корутина для подключение к базе данных Redis."""
    redis.connection = await aioredis.create_redis_pool(
        address=(CONFIG.redis.host, CONFIG.redis.port), minsize=10, maxsize=20,
    )


async def stop_redis():
    """Корутина для отключения от базы данных Redis."""
    redis.connection.close()
    await redis.connection.wait_closed()


async def stop_elasticsearch():
    """Корутина для отключение от базы данных Elasticsearch."""
    await elastic.connection.close()
